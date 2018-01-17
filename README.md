# granulr

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

A super-simple filtering forwarder for GitHub webhooks that lives on Heroku.

Set https://your_hero_app/webhook as the address of a webhook on GitHub, then add any users you want to filter out to the `BOT` config value as a space separated list.

Add event types you want to pass on to `EVENT_TYPES`, or use `*` to pass on everything.

For each event type you've added, add a webhook endpoint to `FORWARDS`.