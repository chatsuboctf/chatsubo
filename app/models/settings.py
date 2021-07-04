from datetime import datetime

from dateutil.tz import UTC, tzutc
from sqlalchemy import func
from sqlalchemy.sql import expression

import app.context

default_homepage = """<button id="home-edit-me" class="pure-material-button-contained" onclick="window.location='/admin/settings/home'" ><svg id="home-edit-me-icon" class="mr-3" viewBox="0 0 24 24">
    <path fill="currentColor" d="M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z" />
</svg>Edit</button>
<center><img class="mt-6" id="home-logo" src="static/uploads/logo/logo.png" /></center>
<pre style="white-space: pre-wrap">
<!-- <center><b id="home-welcome">Welcome on Chatsubo</b></center> -->
<center>
<a href="https://chatsubo.hbouffier.info">-= Getting started =-</a></center>
<center><a href="https://chatsubo.hbouffier.info/docs/Personnalisation/index">-= Customization =-</a></center>
<center><a href="https://chatsubo.hbouffier.info/docs/Personnalisation/index">-= Providers =-</a></center>
<center><a href="https://chatsubo.hbouffier.info/docs/Personnalisation/index">-= Tracks =-</a></center>
<center><a href="https://chatsubo.hbouffier.info/docs/Personnalisation/index">-= Boxes =-</a></center>


</pre>
<style>
#home-edit-me{
    position: absolute;
    right: 15px;
    top: 15px;
}

#home-logo{
    width: 50%;
}

#home-welcome{
    font-size: 24px;
}

#home-edit-me-icon{
    vertical-align: middle;
    text-align: center;
    width:24px;
    height:24px
}

/* From https://codepen.io/finnhvman/pen/MQyJxV */
.pure-material-button-contained {
    position: relative;
    display: inline-block;
    box-sizing: border-box;
    border: none;
    border-radius: 4px;
    padding: 0 16px;
    min-width: 64px;
    height: 40px;
    vertical-align: middle;
    text-align: center;
    text-overflow: ellipsis;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.9);
    background-color: #28303BFF;
    box-shadow: 0 3px 1px -2px rgba(0, 0, 0, 0.2), 0 2px 2px 0 rgba(0, 0, 0, 0.14), 0 1px 5px 0 rgba(0, 0, 0, 0.12);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
    font-size: 14px;
    font-weight: 500;
    line-height: 36px;
    overflow: hidden;
    outline: none;
    cursor: pointer;
    transition: box-shadow 0.2s;
}

.pure-material-button-contained::-moz-focus-inner {
    border: none;
}

/* Overlay */
.pure-material-button-contained::before {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgb(255, 255, 255);
    opacity: 0;
    transition: opacity 0.2s;
}

/* Ripple */
.pure-material-button-contained::after {
    content: "";
    position: absolute;
    left: 50%;
    top: 50%;
    border-radius: 50%;
    padding: 50%;
    width: 32px; /* Safari */
    height: 32px; /* Safari */
    background-color: rgb(255, 255, 255);
    opacity: 0;
    transform: translate(-50%, -50%) scale(1);
    transition: opacity 1s, transform 0.5s;
}

/* Hover, Focus */
.pure-material-button-contained:hover,
.pure-material-button-contained:focus {
    box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.2), 0 4px 5px 0 rgba(0, 0, 0, 0.14), 0 1px 10px 0 rgba(0, 0, 0, 0.12);
}

.pure-material-button-contained:hover::before {
    opacity: 0.08;
}

.pure-material-button-contained:focus::before {
    opacity: 0.24;
}

.pure-material-button-contained:hover:focus::before {
    opacity: 0.3;
}

/* Active */
.pure-material-button-contained:active {
    box-shadow: 0 5px 5px -3px rgba(0, 0, 0, 0.2), 0 8px 10px 1px rgba(0, 0, 0, 0.14), 0 3px 14px 2px rgba(0, 0, 0, 0.12);
}

.pure-material-button-contained:active::after {
    opacity: 0.32;
    transform: translate(-50%, -50%) scale(0);
    transition: transform 0s;
}

/* Disabled */
.pure-material-button-contained:disabled {
    color: rgba(var(--pure-material-onsurface-rgb, 0, 0, 0), 0.38);
    background-color: rgba(var(--pure-material-onsurface-rgb, 0, 0, 0), 0.12);
    box-shadow: none;
    cursor: initial;
}

.pure-material-button-contained:disabled::before {
    opacity: 0;
}

.pure-material-button-contained:disabled::after {
    opacity: 0;
}
</style>"""


class Settings(app.context.db.Model):
    __tablename__ = "settings"

    app_name = app.context.db.Column(
        app.context.db.String(200),
        nullable=False,
        primary_key=True,
        default="Chatsubo"
    )

    default_avatar = app.context.db.Column(
        app.context.db.String(200),
        server_default="/static/img/default_avatar.png"
    )

    homepage = app.context.db.Column(
        app.context.db.Text,
        server_default=default_homepage
    )

    logo = app.context.db.Column(
        app.context.db.String(200),
        server_default="/static/uploads/logo/logo.png"
    )

    logo_width = app.context.db.Column(
        app.context.db.Integer,
        server_default="150"
    )

    logo_height = app.context.db.Column(
        app.context.db.Integer,
        server_default="50"
    )

    enforce_access_restriction = app.context.db.Column(
        app.context.db.Boolean,
        nullable=False,
        server_default=expression.false()
    )

    allow_registration = app.context.db.Column(
        app.context.db.Boolean,
        nullable=False,
        server_default=expression.true()
    )

    enable_teams = app.context.db.Column(
        app.context.db.Boolean,
        nullable=False,
        server_default=expression.true()
    )

    freeze_scoreboard = app.context.db.Column(
        app.context.db.Boolean,
        nullable=False,
        server_default=expression.false()
    )

    not_before = app.context.db.Column(
        app.context.db.DateTime,
        index=False
    )

    not_after = app.context.db.Column(
        app.context.db.DateTime,
        index=False
    )

    def get_ctf_state(self):
        if not self.not_before and not self.not_after:
            return True

        not_before = self.not_before.replace(tzinfo=tzutc())
        not_after = self.not_after.replace(tzinfo=tzutc())
        now = datetime.now(tz=tzutc())

        if not_before < now < not_after:
            return "is_live"
        elif now > not_after:
            return "has_ended"
        elif now < not_before:
            return "not_started"

    def to_json(self):
        return {
            "app_name": self.app_name,
            "homepage": self.homepage,
            "logo": self.logo,
            "logo_width": self.logo_width,
            "logo_height": self.logo_height,
            "default_avatar": self.default_avatar,
            "enforce_access_restriction": self.enforce_access_restriction,
            "enable_teams": self.enable_teams,
            "allow_registration": self.allow_registration,
            "freeze_scoreboard": self.freeze_scoreboard,
            "not_before": self.not_before.isoformat() if self.not_before else None,
            "not_after": self.not_after.isoformat() if self.not_after else None
        }

    def __repr__(self):
        return f"<Settings>"
