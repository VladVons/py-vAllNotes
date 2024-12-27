#!/bin/bash
# Created: 2024.12.27
# Vladimir Vons, VladVons@gmail.com

source ./common.sh


cProject="py-vFS-Note"
cUser="VladVons"
cMail="vladvons@gmail.com"
cUrl="https://github.com/$cUser/$cProject.git"
cBranch="main"


GitAuth()
{
  Log "$0->$FUNCNAME($*)"

  echo "It is not GIT password but SUDO "
  sudo chown -R $USER .

  # sign with eMail
  git config --global user.email "$cMail"
  git config --global user.name "$cUser"

  # save password
  #git config --global credential.helper cache

  # token
  git config --global credential.helper libsecret
  git config --global credential.helper store

  git config -l
}


GitSyncToServ()
{
  aComment="$1";
  Log "$0->$FUNCNAME($*)"

  git status

  git add -u -v
  git commit -a -m "$aComment"

  git push -u origin $cBranch 
}


GitFromServ()
{
  Log "$0->$FUNCNAME($*)"

  git pull
}


GitToServ()
{
  local aComment=${1:-"MyCommit"};
  Log "$0->$FUNCNAME($*)"

  git add -A -v
  GitSyncToServ "$aComment"
}


clear
echo "Repository: $cUrl"
case $1 in
    GitAuth)            "$1"        "$2" "$3" ;;
    GitToServ|t)        GitToServ   "$2" "$3" ;;
    GitFromServ|f)      GitFromServ "$2" "$3" ;;
esac
