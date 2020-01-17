#!/bin/bash
# Pulls and adds files to git before commit
function upload(){
	read -p "Commit description: " desc
	git add . && \
	git add -u && \
	git commit -m "$desc" && \
	git push origin master
}