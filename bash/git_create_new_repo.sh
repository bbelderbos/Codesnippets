#!/bin/bash
# see also http://bobbelderbos.com/2012/03/push-code-remote-web-server-git/

set -e

REPO_DIR=$HOME/repositories
REPO_NAME=$1.git
NEW_REPO=$REPO_DIR/$REPO_NAME

HOOKS_DIR=$NEW_REPO/hooks
POST_RECEIVE=$HOOKS_DIR/post-receive

WORKING_DIR=$2

USER=remote_server_username
DOMAIN=example.com
GITHUB_USER=username

if [ ! -d "$REPO_DIR" ]; then 
	echo -e "$REPO_DIR does not exist, create it first.\n"
	exit 1
fi 

if [ -d "$NEW_REPO" ]; then 
	echo -e "$NEW_REPO already exists.\n"
	exit 1
fi

mkdir $NEW_REPO

if [ ! -d "$NEW_REPO" ]; then 
	echo -e "$NEW_REPO was not created.\n"
	exit $?
fi

cd $NEW_REPO && git init --bare 2>&1

if [ ! -d "$HOOKS_DIR" ]; then
	echo -e "$HOOKS_DIR not found, did git init --bare succeed?\n"
	exit $?
fi

if [ ! -d "$WORKING_DIR" ]; then
	echo -e "$WORKING_DIR not found, creating it now.\n"
	mkdir $WORKING_DIR
	if [ ! -d "$WORKING_DIR" ]; then
		echo -e "$WORKING_DIR still not found, was it created?\n"
		exit $?
	fi
fi

if [ ! -f "$POST_RECEIVE" ]; then
	touch $POST_RECEIVE && chmod 755 $POST_RECEIVE
fi

echo "#!/bin/sh" >> $POST_RECEIVE
echo "GIT_WORK_TREE=$WORKING_DIR git checkout -f" >> $POST_RECEIVE

echo -e "All done, now run the following on your localhost: "
echo -e "  git remote add origin ssh://$USER@$DOMAIN$NEW_REPO "
echo -e "  git push origin +master:refs/heads/master "
echo -e "\nAnd to add a git repo: "
echo -e "  git remote add git git@github.com:$GITHUB_USER/$REPO_NAME"
echo -e "  git push -u git master"

exit 0