#!/bin/bash# Runs Heroku logs
function heroku_logs() {
  heroku login
  # read -p 'App name: ' app
  heroku logs --app 'mecha-senku' --tail
}