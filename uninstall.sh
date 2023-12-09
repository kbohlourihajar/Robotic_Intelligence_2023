sudo apt remove $(cat apt_uninstall.txt)
sudo apt install $(cat apt_reinstall.txt)

pip install -r pip_reinstall.txt
pip list --format freeze | grep -vxFf pip_prev.txt > pip_uninstall.txt
pip uninstall -y -r pip_uninstall.txt

rm pip_uninstall.txt
rm pip_reinstall.txt
rm apt_uninstall.txt
rm apt_reinstall.txt

rm pip_prev.txt
