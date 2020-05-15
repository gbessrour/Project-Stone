#!/bin/bash
# Pulls and adds files to git before commit
function upload(){
	git pull
	read -p "Commit description: " desc
	git add . && \
	git add -u && \
	git commit -m "$desc" && \
	read -p 'Branch: ' branch
	git push origin $branch
}