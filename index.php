<?php
/**
 * CloudApp Webhook - Database only.
 *
 * This file implements the webhook app for CloudApp which inserts a record into
 * the SQLite database only.
 *
 * PHP version 7.3
 *
 * @category  App
 * @package   Index
 * @author    Justin Hartman <j.hartman@ctca.co.za>
 * @copyright 2020 Cape Town Creative Academy (Pty) Limited
 * @license   https://gitlab.com/ctca/cloudapp-webhook/-/blob/master/LICENSE (c)
 * @link      https://gitlab.com/ctca/cloudapp-webhook
 * @since     1.3.0
 */
require_once __DIR__.'/bootstrap.php';

use App\Log;
use App\Database\SqliteConnect;
use App\Database\SqliteInsert;

/**
 * Check the request type
 *
 * @return boolean
 */
function checkMethod()
{
    $request = $_SERVER['REQUEST_METHOD'];
    $allowed = array('POST');

    //Check to see if the current request method isn't allowed.
    if (!in_array($request, $allowed)) {
        header($_SERVER["SERVER_PROTOCOL"] . " 405 Method Not Allowed", true, 405);

        return false;
    }

    return true;
}

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

/**
 * DB Insert
 *
 * @param string $event    The payload event.
 * @param string $itemName The payload item name.
 * @param string $itemUrl  The payload item url.
 * @param string $created  The payload created date.
 *
 * @return void
 */
function dbInsert($event, $itemName, $itemUrl, $created)
{
    // Setup the DB PDO.
    $pdo = (new SqliteConnect())->connect();
    $sqlite = new SqliteInsert($pdo);

    // Build the query
    $insert = $sqlite->insert($event, $itemName, $itemUrl, $created);

    return $insert;
}

// Setup the log file.
$log = new Log;
$logger = $log->logFile();

/**
 * Make sure the method is POST else exit.
 */
try {
    if (checkMethod() === false) {
        throw new Exception('Method not allowed.');
    }
} catch (Exception $e) {
    $logger->error(
        sprintf(
            'Method not allowed. Code: %s. Error: %s.',
            405,
            $e->getMessage()
        )
    );
    echo json_encode(
        array(
        'event' => 'error',
        'code' => 405,
        'payload' =>
            array(
                'error' => $e->getMessage()
            )
        )
    );

    exit;
}

// Create new payload object.
$payload = payload();

// Setup payload variables.
$payloadEvent = $payload['event'];
$payloadName  = $payload['payload']['item_name'];
$payloadUrl   = $payload['payload']['item_url'];
$payloadDate  = $payload['payload']['created_at'];

try {
    dbInsert($payloadEvent, $payloadName, $payloadUrl, $payloadDate);
    $logger->info(
        sprintf(
            'Inserted %s (%s) created at %s into SQLite Database.',
            $payloadName,
            $payloadUrl,
            $payloadDate
        )
    );
} catch (Exception $e) {
    $logger->error(
        sprintf(
            'Index dbInsert error code %s. Error: %s',
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
