function clone_private_repo()
{
	local _repo=$1;
	local _br=$2;
	local _dir=$3;
	local _ro2=`echo "$_repo" | sed 's/gitee.com/bitbucket.org/' | sed "s/:${repopass}@/:${bitbuckettoken}@/"`;
	local _ro3=`echo "$_repo" | sed 's/gitee.com/gitlab.com/'`;

	if [ ! -d "$_dir" ]
	then
		gitclonesucc "$_repo";
		pushd $PWD && cd "$_dir" && git co "$_br" && git remote add origin2 "$_ro2" && \
		git remote add origin3 "$_ro3" && popd;
	fi
}

function clone_public_repo()
{
	local _repo=$1;
	local _br=$2;
	local _dir=$3;
	local _ro2=`echo "$_repo" | sed "s/:${githubtoken}@/:${bitbuckettoken}@/"  | sed 's/github.com/bitbucket.org/'`;

	if [ ! -d "$_dir" ]
	then
		gitclonesucc "$_repo";
		pushd $PWD && cd "$_dir" && git co "$_br" && git remote add origin2 "$_ro2" && \
		popd;
	fi
}

function clone_repo()
{
	local _repo=$1;
	local _dir=$2;

	if [ ! -d "$_dir" ]
	then
		gitclonesucc "$_repo";
	fi
}

