<?php
/**
 * Sqlite Inert.
 *
 * This file implements the Sqlite insert methods.
 *
 * PHP version 7.3
 *
 * @category  App\Classes\Database
 * @package   SqliteInsert
 * @author    Justin Hartman <j.hartman@ctca.co.za>
 * @copyright 2020 Cape Town Creative Academy (Pty) Limited
 * @license   https://gitlab.com/ctca/cloudapp-webhook/-/blob/master/LICENSE (c)
 * @link      https://gitlab.com/ctca/cloudapp-webhook
 * @since     1.3.1
 */
namespace App\Database;

/**
 * Sqlite Insert Class
 *
 * {inheritdoc}
 */
class SqliteInsert
{
    /**
     * PDO instance
     *
     * @var type
     */
    private $pdo;

    /**
     * Initialize the object with a specified PDO object.
     *
     * @param \PDO $pdo Database connection.
     */
    public function __construct($pdo)
    {
        $this->pdo = $pdo;
    }

    /**
     * Insert items.
     *
     * @param string $event    Payload event type.
     * @param string $itemName Payload item name.
     * @param string $itemUrl  Payload item url.
     * @param string $created  Payload created_at date.
     *
     * @return [type] [description]
     */
    public function insert($event, $itemName, $itemUrl, $created)
    {
        $sql = "INSERT INTO payload (
            event,
            payload_item_name,
            payload_item_url,
            payload_created_at,
            created_at,
            downloaded)
            VALUES (
            :event,
            :payload_item_name,
            :payload_item_url,
            :payload_created_at,
            :created_at,
            :downloaded
        )";

        $stmt = $this->pdo->prepare($sql);
        $query = $stmt->execute(
            [
                ':event' => $event,
                ':payload_item_name' => $itemName,
                ':payload_item_url' => $itemUrl,
                ':payload_created_at' => $created,
                ':created_at' => date('Y-m-d H:i:s'),
                ':downloaded' => 0
            ]
        );

        if ($query) {
            $jsonArray = json_encode(
                array(
                    'event'         => 'success',
                    'code'          => 200,
                    'payload'       => array(
                        'id'        => $this->pdo->lastInsertId(),
                        'item_name' => $itemName,
                        'item_url'  => $itemUrl
                    )
                )
            );

            $json = print $jsonArray;
        } else {
            header('Bad Request', true, 400);
            throw new \Exception('📄 ' .$itemName. ' could not be inserted into DB.', 400);
        }

        return $json;
    }
}
