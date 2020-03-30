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

// Set unlimited memory (bad idea).
// ini_set('memory_limit', '-1');
ini_set('memory_limit', '1024M');

// Set the application header to JSON.
header('Content-Type: application/json');

/**
 * Autoload Class
 *
 * @return object Class
 */
function autoload()
{
    include_once getcwd()."/classes/Download.php";
    include_once getcwd()."/classes/Log.php";
    include_once getcwd()."/classes/Upload.php";
}

// Autoload the Class files.
spl_autoload_register("autoload");
