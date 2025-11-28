if [ -d .git ];then
	rm -rf ./.git
else
	echo "Repositório git não existente"
	exit 1
fi

if [ -z "$1" ];then
	echo "Digite o link do repositório como argumento"
	exit1
fi

git init
git add .
git commit -m "chore: init"
git branch -M main
git remote add origin $1
git push -u origin main
