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
namespace App;

use App\Log;

/**
 * Google Drive Upload Class
 *
 * {inheritdoc}
 */
class Upload
{
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

    /**
     * Returns an authorized API client.
     *
     * @return Google_Client the authorized client object
     */
    public function getClient()
    {
        // putenv('GOOGLE_APPLICATION_CREDENTIALS=./.credentials.json');
        // putenv('GOOGLE_APPLICATION_CREDENTIALS=/lamp0/web/vhosts/cloudapp.hartman.me/credentials.json');
        putenv('GOOGLE_APPLICATION_CREDENTIALS=/lamp0/web/includes/credentials.json');
        $client = new \Google_Client();
        $client->setApplicationName('CloudApp for Google Drive');
        $client->useApplicationDefaultCredentials();
        $client->addScope(\Google_Service_Drive::DRIVE);

        return $client;
    }

    /**
     * Upload video.
     *
     * @param Google_Service_Drive_DriveFile $path The file to upload.
     * @param string                         $name The name of the file.
     *
     * @return Google_Service_Exception Throw error on upload.
     *         Monolog\Logger           Log upload to app log file.
     *         object                   JSON response.
     */
    public function uploadVideo($path, $name)
    {
        // Setup the log file.
        $log = new Log;
        $logger = $log->logFile();

        // Use getClient() method to setup Google Authorised Client object.
        $client = $this->getClient();

        // Log new token response.
        $callback = $log->getTokenCallback();
        $client->setTokenCallback($callback);

        // Create Google Drive service.
        $service = new \Google_Service_Drive($client);
        // Define the "Media Uploads" team drive.
        $parent  = "0AMzDjXZ2bebtUk9PVA";

        // Define type of file by extension.
        $extType = substr($name, -3, 3);
        if ($extType === "png") {
            $desc = "Image file uploaded from CloudDrive to Google Drive.";
            $mime = "image/png";
        } elseif ($extType === "mov") {
            $desc = "Video file uploaded from CloudDrive to Google Drive.";
            $mime = "video/quicktime";
        }

        // Set up the file details.
        $file = new \Google_Service_Drive_DriveFile(
            array(
                'name'        => $name,
                'description' => $desc,
                'mimeType'    => $mime,
                'teamDriveId' => $parent,
                'driveId'     => $parent,
                'parents'     => [
                    $parent
                ],
            )
        );

        // Load the file from disk.
        $data = file_get_contents($path);

        // Setup options for the upload including the data payload.
        $options = array(
            'supportsAllDrives' => true, // so important for this app to work.
            'data'              => $data,
            'mimeType'          => 'application/octet-stream',
            'uploadType'        => 'resumable'
        );

        // Try upload the file else throw exception.
        try {
            // Upload and create the file.
            $createdFile = $service->files->create($file, $options);

            // Log the upload data.
            $logger->info(
                sprintf('File Name: %s', $createdFile['name'])
            );
            $logger->info(
                sprintf(
                    'Drive Link: https://drive.google.com/open?id=%s',
                    $createdFile['id']
                )
            );

            // JSON payload.
            $payload = array(
                'event'         => 'success',
                'code'          => 200,
                'payload'       => array(
                    'id'        => $createdFile['id'],
                    'name'      => $createdFile['name'],
                    'drive_url' => 'https://drive.google.com/open?id='.$createdFile['id']
                )
            );
            // Encode JSON payload.
            $json = json_encode($payload);
        } catch (\Google_Service_Exception $e) {
            // Log the error
            $logger->error($e->getMessage());
            // JSON payload.
            $json = $e->getMessage();
        }
        // Build the JSON message.
        $message = print $json;

        return $message;
    }
}
/**
 * Run the method.
 */
// uploadVideo();
