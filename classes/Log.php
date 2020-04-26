<?php
/**
 * Log file.
 *
 * Methods to log items to the log file.
 *
 * PHP version 7.3
 *
 * @category  App\Classes
 * @package   Log
 * @author    Justin Hartman <j.hartman@ctca.co.za>
 * @copyright 2020 Cape Town Creative Academy (Pty) Limited
 * @license   https://gitlab.com/ctca/cloudapp-webhook/-/blob/master/LICENSE (c)
 * @link      https://gitlab.com/ctca/cloudapp-webhook
 * @since     0.1.0
 */
namespace App;

use Monolog\Logger;
use Monolog\Handler\StreamHandler;

/**
 * Log Class
 *
 * {inheritdoc}
 */
class Log
{
    /**
     * Setup new logger object and log file.
     *
     * @return Monolog\Logger|Monolog\Handler\StreamHandler
     */
    public function logFile()
    {
        $logger = new Logger('App');
        $logger->pushHandler(new StreamHandler('logs/app.log', Logger::DEBUG));

        return $logger;
    }

    /**
     * Logs the token callback.
     *
     * @return Monolog\Logger Log cache key receiving new token.
     */
    public function getTokenCallback()
    {
        $logger = $this->logFile();

        // Client token callback method.
        $callback = function ($cacheKey, $accessToken) use ($logger) {
            $logger->debug(sprintf('New token received at cache key %s', $cacheKey));
        };

        return $callback;
    }

    /**
     * Log headers to file.
     *
     * @return void
     */
    public function logHeaders()
    {
        $myFile = "logs/headers.log";
        $date = date('Y-m-d H:i:s');
        $fh = fopen($myFile, 'a') or die("can't open file");
        fwrite($fh, "\n----------------------------------------------------\n");
        fwrite($fh, "🕒 ".$date);
        fwrite($fh, "\n");
        foreach ($_SERVER as $h => $v) {
            if (preg_match('/HTTP_(.+)/', $h, $hp)) {
                fwrite($fh, "$h = $v\n");
            }
        }
        fwrite($fh, "\r\n");
        fwrite($fh, file_get_contents('php://input'));
        fclose($fh);
    }

    /**
     * Log request body.
     *
     * @return void
     */
    public function logRequest()
    {
        $myFile = "logs/request.log";
        $date = date('Y-m-d H:i:s');
        $fh = fopen($myFile, 'a') or die("can't open file");
        fwrite($fh, "\n----------------------------------------------------\n");
        fwrite($fh, "🕒 ".$date);
        fwrite($fh, "\n");
        fwrite($fh, file_get_contents('php://input'));
        fclose($fh);
    }
}
