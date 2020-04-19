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
use App\Mail;
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
 * @return array JSON Array object.
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
 * @param string $event   The payload event.
 * @param string $name    The payload item name.
 * @param string $url     The payload item url.
 * @param string $created The payload created date.
 *
 * @return App\Database\SqliteInsert
 */
function dbInsert(string $event, string $name, string $url, string $created)
{
    // Setup the DB PDO.
    $pdo = (new SqliteConnect())->connect();
    $sqlite = new SqliteInsert($pdo);

    // Build the query
    $insert = $sqlite->insert($event, $name, $url, $created);

    return $insert;
}

/**
 * Sends email.
 *
 * @param object $logger  The log file object.
 * @param string $subject The email subject.
 * @param string $body    The email body.
 *
 * @return App\Log Log the success or error to the log file.
 */
function sendMail(object $logger, string $subject, string $body)
{
    $conn = (new Mail())->connect();
    $recipient = array(
        'name' => 'Justin Hartman',
        'email' => 'j.hartman@ctca.co.za'
    );

    try {
        $mail = new Mail;
        $mail->send($conn, $recipient, $subject, $body);
        $log = $logger->info(sprintf('PHPMailer Sent: %s', $subject));
    } catch (Exception $e) {
        $log = $logger->error(sprintf('PHPMailer Error: %s', $e->getMessage()));
    }

    return $log;
}

/**
 * Commit database to git repo.
 *
 * @param object $logger   The log file object.
 *
 * @return App\Log Log the success or error to the log file.
 */
function gitCommit(object $logger)
{
    try {
        shell_exec('/bin/bash /app/bin/webhook.sh');
        $log = $logger->info('Committed Database to Git Repo.');
    } catch (Exception $e) {
        $log = $logger->error(sprintf('Git Commit Error: %s', $e->getMessage()));
    }

    return $log;
}

/**
 * Setup Log file instance.
 *
 * @var App\Log
 */
$log = new Log;
$logger = $log->logFile();

/**
 * Log raw headers to file.
 */
$log->logHeaders();
$log->logRequest();

/**
 * Test for POST else exit.
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
    $jsonArray = json_encode(
        array(
        'event' => 'error',
        'code' => 405,
        'payload' =>
            array(
                'error' => $e->getMessage()
            )
        )
    );

    $json = print $jsonArray;

    return $json;
}

// Create new payload object.
$payload = payload();

// Setup payload variables.
$payloadEvent = $payload['event'];
$payloadName  = $payload['payload']['item_name'];
$payloadUrl   = $payload['payload']['item_url'];
$payloadDate  = $payload['payload']['created_at'];

/**
 * Insert record to DB.
 *
 * Try to insert the record to the database. If successful, log a info message
 * and send an email with success details. If failed, log an error message, send
 * an email with error details and return an error JSON object.
 */
try {
    $insert = dbInsert($payloadEvent, $payloadName, $payloadUrl, $payloadDate);
    if ($insert) {
        // Build success messages.
        $mailSubSuccess = $payloadName . " Inserted into DB";
        $successMessage = sprintf(
            'Inserted %s (%s) created at %s into SQLite Database.',
            $payloadName,
            $payloadUrl,
            $payloadDate
        );
        // Log error to Monolog.
        $logger->info($successMessage);
        // Send success mail.
        sendMail($logger, $mailSubSuccess, $successMessage);
        // Commit DB to git repo.
        gitCommit($logger);
    }
} catch (Exception $e) {
    // Build error messages.
    $mailSubError = $payloadName . " dbInsert error";
    $errorMessage = sprintf(
        'Index dbInsert error code %s. Error: %s',
        $e->getCode(),
        $e->getMessage()
    );

    // Log error to Monolog.
    $logger->error($errorMessage);
    // Send error mail.
    sendMail($logger, $mailSubError, $errorMessage);

    // Echo JSON object.
    $jsonArray = json_encode(
        array(
        'event' => 'error',
        'code' => $e->getCode(),
        'payload' =>
            array(
                'error' => $e->getMessage()
            )
        )
    );

    $json = print $jsonArray;

    return $json;
}
