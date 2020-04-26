<?php
/**
 * PhpAmqpLib Message Queue Class.
 *
 * Methods to run the AMQP message queue.
 *
 * Run with:
 * $ampq = new MessageQueue();
 * $conn = $ampq->connection();
 * $ampq->amqpMessage($conn, 'app.webhook', 'direct', 'python', "Message text");
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
    /**
     * CloudAMQP connection.
     *
     * @return \PhpAmqpLib\Connection\AMQPStreamConnection
     */
    public function connection()
    {
        $url = parse_url(
            getenv(
                'CLOUDAMQP_URL',
                'amqp://guest:guest@localhost//'
            )
        );

        $conn = new AMQPStreamConnection(
            $url['host'],
            5672,
            $url['user'],
            $url['pass'],
            substr(
                $url['path'],
                1
            )
        );

        return $conn;
    }

    /**
     * AMQP message send.
     *
     * @param object $conn     The CloudAMQP connection.
     * @param string $exchange The exchange.
     * @param string $type     The exchange type one of direct, fanout,
     *                         headers, or topic.
     * @param string $queue    The queue name.
     * @param string $text     The text for the message.
     *
     * @return string The status and message.
     */
    public function amqpMessage($conn, $exchange, $type, $queue, $text)
    {
        $channel = $conn->channel();

        $channel->queue_declare($queue, true, true, true, false, false);
        $channel->exchange_declare($exchange, $type, true, true, false, false, false);
        $channel->queue_bind($queue, $exchange);

        $message = new AMQPMessage(
            $text,
            array(
                'content_type' => 'text/plain',
                'delivery_mode' => 2
            )
        );
        $channel->basic_publish($message, $exchange);

        $channel->close();
        // $conn->close();

        $status = print(" ✅ '".$text."' sent to AMQP Stream.");

        return $status;
    }
}
