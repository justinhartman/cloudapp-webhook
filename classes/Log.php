<?php
namespace App;

use Monolog\Logger;
use Monolog\Handler\StreamHandler;

/**
 * File Download Class
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
     * @param object $logger The logFile() method object.
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
}
