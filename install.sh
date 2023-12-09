grep -o '^[^#]*' apt_requirements.txt > "apt_requirements.no_comments.txt"

sudo apt list --installed > "apt_prev.txt"
pip list --format freeze > "pip_prev.txt"

sudo apt install -y $(cat apt_requirements.no_comments.txt)
pip install -r pip_requirements.txt

sudo apt list --installed > "apt_post.txt"
pip list --format freeze > "pip_post.txt"

cat apt_prev.txt | grep -vxFf apt_post.txt > "apt_reinstall.txt"
cat apt_post.txt | grep -vxFf apt_prev.txt > "apt_uninstall.txt"
cat pip_prev.txt | grep -vxFf pip_post.txt > "pip_reinstall.txt"

rm apt_requirements.no_comments.txt
rm apt_prev.txt
rm apt_post.txt
rm pip_post.txt
