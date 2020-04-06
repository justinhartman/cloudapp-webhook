<?php
/**
 * Bootstrap
 *
 * PHP version 7.3
 *
 * @category  App
 * @package   Base
 * @author    Justin Hartman <j.hartman@ctca.co.za>
 * @copyright 2020 Cape Town Creative Academy (Pty) Limited
 * @license   https://gitlab.com/ctca/cloudapp-webhook/-/blob/master/LICENSE (c)
 * @link      https://gitlab.com/ctca/cloudapp-webhook
 * @since     0.1.0
 */
require_once __DIR__.'/vendor/autoload.php';

/**
 * PHP configuration.
 */
ini_set('memory_limit', '-1');
ini_set('date.timezone', 'Africa/Johannesburg');

/**
 * HTTP Headers - Set the application header to JSON.
 */
header('Content-Type: application/json');

/**
 * Path to the sqlite file.
 */
const SQLITE_DATABASE = 'database/database.sqlite';

/**
 * General Mail settings.
 */
const MAIL_HOST = 'smtp.mailgun.org';
const MAIL_USER = 'ctca@mail.fightspam.email';
const MAIL_PASS = 'dbf388c574dc4d63fa5c5b4d51d47866-aa4b0867-edb535ef';
const MAIL_PORT = 587;
const MAIL_FROM_NAME = 'Creative Academy';
const MAIL_FROM_ADDRESS = 'noreply@ctca.co.za';
const MAIL_DEBUG = false;

/**
 * Autoload Class
 *
 * @return object Class
 */
function autoload()
{
    include_once getcwd()."/classes/Download.php";
    include_once getcwd()."/classes/Log.php";
    include_once getcwd()."/classes/Mail.php";
    include_once getcwd()."/classes/Database/SqliteConnect.php";
    include_once getcwd()."/classes/Database/SqliteInsert.php";
    include_once getcwd()."/classes/Upload.php";
}

// Autoload the Class files.
spl_autoload_register("autoload");
