import json
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import yaml


class Emailer:
    """
    Presentation logic and emailing the receivers is defnied here
    """

    def __init__(self, data, vaccine):
        self.data = json.loads(data)
        self.vaccine = vaccine

    def prepare_html(self, data, email, vaccine):
        """
        Prepares and returns a string containing the data inside html elements
        :param email: Receiver email
        :param vaccine: preferred vaccine (filtered by this vaccine)
        :param data: JSON object of filtered data results
        :return:
        """
        html = f"""\
                           <html>
                             <head></head>
                             <body style="font-family:helvetica;">
                                <table style="font-family:helvetica;"><td>
                                  <p><b>Hi! {email}<br><br>
                                      Here is the Covid vaccination center info giving {vaccine} in district: BBMP</b><br>\n\n
                           """
        for center in data["centers"]:
            html += "\n<br><b>CENTER</b><br><br>\n"
            for key in center:
                if key == "sessions":
                    for session in center["sessions"]:
                        html += "\n<br><b>&emsp;&emsp;SESSION</b><br><br>\n"
                        for session_key in session:
                            if session_key == "slots":
                                html += f"&emsp;&emsp;&emsp;{session_key.replace('_', ' ').title()} :<br>"
                                for slots in session[session_key]:
                                    html += "&emsp;&emsp;&emsp;&emsp;" + slots + "<br>"
                            else:
                                html += f"&emsp;&emsp;&emsp;{session_key.replace('_', ' ').title()} : {session[session_key]}<br>\n"
                else:
                    html += f"&nbsp;{key.replace('_', ' ').title()} : {center[key]}<br>\n"
        html += "<br><br><b>VACCINE STATS</b><br>\n"
        vaccine_stats = data["Vaccine_Stats"]
        for state in vaccine_stats:
            html += f"<br><b>{state}: </b><br><br>\n"
            for metrics in vaccine_stats[state]:
                stat_vals = vaccine_stats[state][metrics]
                html += f"{metrics} : {int(stat_vals['value'])} ( <span style='color:green;'><b> {'{:0.2f}'.format(stat_vals['change_per'])}%</b> </span> )<br>\n(<span style='color:green;'><b>{'{:0.2f}'.format(stat_vals['tot_percentage'])}% </b></span> of <b>{state}</b>)<br><br>\n "
        html += "<br><br><b>CASE STATS</b><br>\n"
        vaccine_stats = data["Case_Stats"]
        for state in vaccine_stats:
            html += f"<br><b>{state}: </b><br><br>\n"
            for metrics in vaccine_stats[state]:
                stat_vals = vaccine_stats[state][metrics]
                if metrics != "Recovered":
                    color = 'red' if stat_vals['change_per'] > 0 else 'green'
                else:
                    color = 'green' if stat_vals["change_per"] > 0 else 'red'
                html += f"{metrics} : {int(stat_vals['value'])} ( <span style='color:{color};'><b> {'{:0.2f}'.format(stat_vals['change_per'])}%</b> </span> )<br>\n(<span style='color:{color};'><b>{'{:0.2f}'.format(stat_vals['tot_percentage'])}% </b></span> of <b>{state}</b>)<br><br>\n "

        html += """
                       </p>
                       </td>
                       </table>
                   </body>
               </html>"""
        return html

    def prepare_message(self, html, email):
        """
        Prepares the message with the right HTML format and proper
        to and from addresses and subject
        :return:
        """

        # Create the body of the message (a plain-text and an HTML version).
        message = MIMEMultipart('alternative')
        message['Subject'] = "Covid Vaccine Info"
        message['From'] = "Covid Notification"
        message['To'] = email
        """
        # For debugging purposes
        with open("sample.html", 'w') as file:
            file.write(html)
        """
        part = MIMEText(html, 'html')
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        message.attach(part)
        return message

    def send_vaccine_info(self):
        """
        Co-ordinates all of the methods in class.
        :param district_id: The district_id used in the API
        :param vaccine: the vaccine to filter by
        :return:
        """
        if self.data["updated"] == "no":
            if self.data["updated"] == "no":
                print("Email not sent")
                return -1
        receiver_email = self.get_receiver_emails()
        messages = []
        for email in receiver_email:
            html = self.prepare_html(self.data, email, self.vaccine)
            message = self.prepare_message(html, email)
            messages.append(message)
        self.send_email(receiver_email, messages)

    def send_email(self, receiver_email, messages):
        """
        Sends email containing messages to receiver emails
        :param messages: The messages
        :param receiver_email:  list of emails
        :return:
        """
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = self.get_email_credentials()[0]
        password = self.get_email_credentials()[1]
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            for email, message in zip(receiver_email, messages):
                # print(sender_email, email, message)
                server.sendmail(sender_email, email, message.as_string())

    def get_receiver_emails(self):
        """
        Retrieves the receiver emails from YAML config
        :return: List of emails
        """
        with open("emails.yaml", "r") as email_config:
            return yaml.load(email_config.read(), Loader=yaml.FullLoader)

    def get_email_credentials(self):
        """
        Retrieves the credentials from YAML file
        :return: List of email and pass
        """
        with open("email_cred.yaml", "r") as email_config:
            return yaml.load(email_config.read(), Loader=yaml.FullLoader)
