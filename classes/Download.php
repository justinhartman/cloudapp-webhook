<?php
/**
 * Download with cURL.
 *
 * Downloads media from CloudApp to server.
 *
 * PHP version 7.3
 *
 * @category  App
 * @package   Download
 * @author    Justin Hartman <j.hartman@ctca.co.za>
 * @copyright 2020 Cape Town Creative Academy (Pty) Limited
 * @license   https://gitlab.com/ctca/cloudapp-webhook/-/blob/master/LICENSE (c)
 * @link      https://gitlab.com/ctca/cloudapp-webhook
 * @since     0.0.1
 */
namespace App;

use App\Log;
use Exception;

/**
 * File Download Class
 *
 * {inheritdoc}
 */
class Download
{
    /**
     * Download URL.
     *
     * @param string $url Original Payload URL.
     *
     * @return string Returns a download URL.
     */
    public function downloadUrl($url)
    {
        $replace   = 'https://media.ctca.co.za/';
        $payloadId = str_replace($replace, null, $url);

        $link = "https://media.ctca.co.za/items/".$payloadId."/download";

        return $link;
    }

    /**
     * Save path.
     *
     * Sets the full path and filename to save the media on the server.
     *
     * @param string $name Payload item file name.
     *
     * @return string|Exception String containing the path to save the file to.
     */
    public function saveTo($name)
    {
        // Setup the log file.
        $log = new Log;
        $logger = $log->logFile();

        // Get file extension.
        $extType = substr($name, -3, 3);

        try {
            if ($extType === "png") {
                $folder = getcwd()."/media/images/".$name;
            } elseif ($extType === "mov") {
                $folder = getcwd()."/media/videos/".$name;
            } else {
                throw new Exception(
                    "Error Processing Request.",
                    400
                );
            }
        } catch (Exception $e) {
            $logger->error(
                sprintf(
                    'Download saveTo method. Code: %s. Error: %s.',
                    $e->getCode(),
                    $e->getMessage()
                )
            );
            echo json_encode(
                array(
                'event' => 'error',
                'code' => $e->getCode(),
                'payload' => array(
                    'error' => 'Download saveTo method error: ' . $e->getMessage()
                )
                )
            );

            exit;
        }

        return $folder;
    }
}
