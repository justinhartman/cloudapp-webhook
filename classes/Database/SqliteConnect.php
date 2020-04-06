<?php
/**
 * Sqlite Connect.
 *
 * This file implements the Sqlite connect methods.
 *
 * PHP version 7.3
 *
 * @category  App\Classes\Database
 * @package   SqliteConnect
 * @author    Justin Hartman <j.hartman@ctca.co.za>
 * @copyright 2020 Cape Town Creative Academy (Pty) Limited
 * @license   https://gitlab.com/ctca/cloudapp-webhook/-/blob/master/LICENSE (c)
 * @link      https://gitlab.com/ctca/cloudapp-webhook
 * @since     1.3.1
 */
namespace App\Database;

/**
 * Sqlite Connect Class
 *
 * {inheritdoc}
 */
class SqliteConnect
{
    /**
     * PDO instance
     *
     * @var type
     */
    private $pdo;

    /**
     * Return instance of the PDO object that connects to the SQLite database.
     *
     * @return \PDO
     */
    public function connect()
    {
        if ($this->pdo == null) {
            $this->pdo = new \PDO("sqlite:" . SQLITE_DATABASE);
        }

        return $this->pdo;
    }
}
