<?php
/**
 * CloudApp Webhook.
 *
 * This file implements the webhook for CloudApp.
 *
 * PHP version 7.3
 *
 * @category  App
 * @package   Index
 * @author    Justin Hartman <j.hartman@ctca.co.za>
 * @copyright 2020 Cape Town Creative Academy (Pty) Limited
 * @license   https://gitlab.com/ctca/cloudapp-webhook/-/blob/master/LICENSE (c)
 * @link      https://gitlab.com/ctca/cloudapp-webhook
 * @since     0.0.1
 */
require_once __DIR__.'/bootstrap.php';

use App\Upload;
use App\Download;
use App\Log;

/**
 * JSON Payload.
 *
 * @return array Array object from the JSON payload.
 */
function payload()
{
    $json = file_get_contents('php://input');
    $data = json_decode($json, true);

    return $data;
}

// Create new payload object.
$payload = payload();

// Setup payload variables.
$payloadEvent = $payload['event'];
$payloadName  = $payload['payload']['item_name'];
$payloadUrl   = $payload['payload']['item_url'];

// Load classes.
$download = new Download;
$upload   = new Upload;

// Get download URL from the Payload URL.
$fileUrl = $download->downloadUrl($payloadUrl);

// Save media to file path.
$savePath = $download->saveTo($payloadName);


try {
    //Open file handler.
    $file = fopen($savePath, 'w+');

    //If $file is FALSE, something went wrong.
    if ($file === false) {
        throw new Exception('Could not open: ' . $savePath);
    }
} catch (Exception $e) {
    $logger->error(
        sprintf(
            'Index savePath error. Code: %s. Error: %s.',
            $e->getCode(),
            $e->getMessage()
        )
    );
    echo json_encode(
        array(
        'event' => 'error',
        'code' => $e->getCode(),
        'payload' =>
            array(
                'error' => $e->getMessage()
            )
        )
    );

    exit;
}

try {
    //Create a cURL handle.
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $fileUrl);

    // Options
    curl_setopt($ch, CURLOPT_VERBOSE, 1);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_AUTOREFERER, false);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_REFERER, "https://media.ctca.co.za");
    curl_setopt($ch, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1);
    curl_setopt($ch, CURLOPT_HEADER, 0);

    //Pass our file handle to cURL.
    // curl_setopt($ch, CURLOPT_FILE, $file);

    //Timeout if the file doesn't download after 20 seconds.
    // curl_setopt($ch, CURLOPT_TIMEOUT, 60);

    //Execute the request.
    // curl_exec($ch);
    $result = curl_exec($ch);

    //If there was an error, throw an Exception
    if (curl_errno($ch)) {
        throw new Exception(curl_error($ch));
    }
} catch (Exception $e) {
    $logger->error(
        sprintf(
            'Index cURL error. Code: %s. Error: %s.',
            $e->getCode(),
            $e->getMessage()
        )
    );
    echo json_encode(
        array(
        'event' => 'error',
        'code' => $e->getCode(),
        'payload' =>
            array(
                'error' => $e->getMessage()
            )
        )
    );

    exit;
}

//Get the HTTP status code.
$statusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

fwrite($file, $result);

//Close the cURL handler.
curl_close($ch);

//Close the file handler.
fclose($file);

if ($statusCode == 200) {
    return $upload->uploadVideo($savePath, $payloadName);
} else {
    $logger->error(
        sprintf(
            'Index statusCode error. Code: %s. There was an error with the download request.',
            $statusCode
        )
    );
    // JSON payload.
    echo json_encode(
        array(
        'event' => 'error',
        'code' => $statusCode,
        'payload' =>
            array(
                'There was an error with the download request.'
            )
        )
    );

    exit;
}
