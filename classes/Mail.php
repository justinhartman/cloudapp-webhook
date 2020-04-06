<?php
/**
 * Mailer.
 *
 * This file implements the mailer methods to send email.
 *
 * PHP version 7.3
 *
 * @category  App\Classes
 * @package   Mail
 * @author    Justin Hartman <j.hartman@ctca.co.za>
 * @copyright 2020 Cape Town Creative Academy (Pty) Limited
 * @license   https://gitlab.com/ctca/cloudapp-webhook/-/blob/master/LICENSE (c)
 * @link      https://gitlab.com/ctca/cloudapp-webhook
 * @since     2.0.1
 */
namespace App;

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;
use PHPMailer\PHPMailer\SMTP;

/**
 * Mail Class
 *
 * {inheritdoc}
 */
class Mail
{
    /**
     * PHPMailer instance
     *
     * @var type
     */
    private $mail;

    /**
     * Return PHPMailer instance.
     *
     * @return \PHPMailer\PHPMailer\PHPMailer
     */
    public function connect()
    {
        if ($this->mail == null) {
            // Create a new PHPMailer instance
            $this->mail = new PHPMailer(true);
            // Tell PHPMailer to use SMTP
            $this->mail->isSMTP();

            // Enable SMTP debugging
            $debug = MAIL_DEBUG;
            if ($debug === true) {
                $this->mail->SMTPDebug = SMTP::DEBUG_SERVER;
            } else {
                $this->mail->SMTPDebug = SMTP::DEBUG_OFF;
            }
            $this->mail->Host = MAIL_HOST;
            $this->mail->Port = MAIL_PORT;
            $this->mail->SMTPAuth = true;
            $this->mail->Username = MAIL_USER;
            $this->mail->Password = MAIL_PASS;
        }

        return $this->mail;
    }

    /**
     * Send email.
     *
     * @param PHPMailer $mail      PHPMailer object
     * @param array     $recipient Recipient name and email.
     * @param string    $subject   Subject of the email.
     * @param string    $message   Body of the email.
     *
     * @return True|PHPMailer\PHPMailer\Exception
     */
    public function send(PHPMailer $mail, array $recipient, string $subject, string $message)
    {
        // Set who the message is to be sent from
        $mail->setFrom(MAIL_FROM_ADDRESS, MAIL_FROM_NAME);
        // Set who the message is to be sent to
        $mail->addAddress($recipient['email'], $recipient['name']);
        // Set the subject line
        $mail->Subject = $subject;
        // Create body from variable.
        $mail->Body = $message;
        // Replace message text with the plain text body.
        $altMessage = trim(strip_tags($message));
        $mail->AltBody = $altMessage;

        //send the message, check for errors
        if (!$mail->send()) {
            return $mail->ErrorInfo;
        } else {
            return true;
        }
    }
}
