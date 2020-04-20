<?php
/**
 * PhpAmqpLib Message Queue Class.
 *
 * Methods to run the AMQP message queue.
 *
 * Run with:
 * $ampq = new MessageQueue();
 * $conn = $ampq->connection();
 * $ampq->amqpMessage($conn, 'python_queue', "Testing 1-2-3.");
 *
 * PHP version 7.3
 *
 * @category  App\Classes
 * @package   MessageQueue
 * @author    Justin Hartman <j.hartman@ctca.co.za>
 * @copyright 2020 Cape Town Creative Academy (Pty) Limited
 * @license   https://gitlab.com/ctca/cloudapp-webhook/-/blob/master/LICENSE (c)
 * @link      https://gitlab.com/ctca/cloudapp-webhook
 * @since     3.2.1
 */
namespace App;

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

/**
 * MessageQueue Class
 *
 * {inheritdoc}
 */
class MessageQueue
{
    public function connection()
    {
        $url = parse_url(getenv('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//'));
        $connection = new AMQPStreamConnection($url['host'], 5672, $url['user'], $url['pass'], substr($url['path'], 1));
        $channel = $connection->channel();

        return $channel;
    }

    public function amqpMessage($conn, $queue, $message)
    {
        $conn->queue_declare($queue, false, false, false, false);

        $msg = new AMQPMessage($message);
        $conn->basic_publish($msg, '', $queue);

        $conn->close();
        $connection->close();

        $status = " [x] Callback sent to AMQP Stream.\n";

        return $status;
    }
}
