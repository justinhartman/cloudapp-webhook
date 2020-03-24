<?php
/**
 * Upload files to Drive API.
 *
 * This file implements the file upload method to Google Drive.
 *
 * PHP version 7.3
 *
 * @category  App
 * @package   Upload
 * @author    Justin Hartman <j.hartman@ctca.co.za>
 * @copyright 2020 Cape Town Creative Academy (Pty) Limited
 * @license   https://gitlab.com/ctca/cloudapp-webhook/-/blob/master/LICENSE (c)
 * @link      https://gitlab.com/ctca/cloudapp-webhook
 * @since     0.0.1
 */
require_once __DIR__.'/vendor/autoload.php';

/**
 * App caching.
 *
 * This adds caching to the app but it's not implemented.
 *
 * @todo run this command: `composer require cache/filesystem-adapter`
 * @todo uncomment the lines below.
 */
// use League\Flysystem\Adapter\Local;
// use League\Flysystem\Filesystem;
// use Cache\Adapter\Filesystem\FilesystemCachePool;

// $filesystemAdapter = new Local(__DIR__.'/');
// $filesystem        = new Filesystem($filesystemAdapter);

// $cache = new FilesystemCachePool($filesystem);
// $client->setCache($cache);

use Monolog\Logger;
use Monolog\Handler\StreamHandler;

/**
 * Returns an authorized API client.
 *
 * @return Google_Client the authorized client object
 */
function getClient()
{
    putenv('GOOGLE_APPLICATION_CREDENTIALS=./credentials.json');
    $client = new Google_Client();
    $client->setApplicationName('CloudApp for Google Drive');
    $client->useApplicationDefaultCredentials();
    $client->addScope(Google_Service_Drive::DRIVE);

    return $client;
}

/**
 * Setup new logger object and log file.
 *
 * @return Monolog\Logger|Monolog\Handler\StreamHandler
 */
function logFile()
{
    $logger = new Logger('App');
    $logger->pushHandler(new StreamHandler('logs/app.log', Logger::DEBUG));

    return $logger;
}
/**
 * Logs the token callback.
 *
 * @param object $logger The logFile() method object.
 *
 * @return Monolog\Logger Log cache key receiving new token.
 */
function getTokenCallback($logger)
{
    // Client token callback method.
    $callback = function ($cacheKey, $accessToken) use ($logger) {
        $logger->debug(sprintf('New token received at cache key %s', $cacheKey));
    };

    return $callback;
}

/**
 * Upload video.
 *
 * @return Google_Service_Exception Throw error on upload.
 *         Monolog\Logger           Log upload to app log file.
 *         object                   JSON response.
 */
function uploadVideo()
{
    // Use getClient() method to setup Google Authorised Client object.
    $client = getClient();

    // Setup the log file from method.
    $logger = logFile();

    // Log new token response.
    $callback = getTokenCallback($logger);
    $client->setTokenCallback($callback);

    // Create Google Drive service.
    $service = new Google_Service_Drive($client);
    // Define the "Media Uploads" team drive.
    $parent = "0AMzDjXZ2bebtUk9PVA";

    // Set up the file details.
    $file = new Google_Service_Drive_DriveFile(
        array(
            'name' => uniqid().'.mov',
            'description' => 'A Video uploaded from CloudApp.',
            'mimeType' => 'video/quicktime',
            'teamDriveId' => $parent,
            'driveId' => $parent,
            'parents' => [
                $parent
            ],
        )
    );

    // Load the file from disk.
    $data = file_get_contents('media/1_4mb.mov');

    // Setup options for the upload including the data payload.
    $options = array(
        'supportsAllDrives' => true, // so important for this app to work.
        'data' => $data,
        'mimeType' => 'application/octet-stream',
        'uploadType' => 'resumable'
    );

    // Try upload the file else throw exception.
    try {
        // Upload and create the file.
        $createdFile = $service->files->create($file, $options);

        // Log the upload data.
        $logger->info(sprintf('Video Name: %s', $createdFile['name']));
        $logger->info(sprintf('Drive Link: https://drive.google.com/open?id=%s', $createdFile['id']));

        // JSON payload.
        $payload = array(
            'event' => 'success',
            'code' => 200,
            'payload' => array(
                'id' => $createdFile['id'],
                'name' => $createdFile['name'],
                'drive_url' => 'https://drive.google.com/open?id='.$createdFile['name']
            )
        );
        // Encode JSON payload.
        $json = json_encode($payload);
    } catch (Google_Service_Exception $e) {
        // Log the error
        $logger->error($e->getMessage());
        // JSON payload.
        $json = $e->getMessage();
    }

    $message = print $json;

    return $message;
}

/**
 * Run the method.
 */
uploadVideo();
