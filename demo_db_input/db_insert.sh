# mysql -uroot -p"54321" -e "CREATE USER 'userExample'@'db' IDENTIFIED BY '54321';"
# echo "Granting privileges..."
# mysql -uroot -p"54321" -e "GRANT ALL PRIVILEGES ON *.* TO 'userExample'@'db';"
# mysql -uroot -p"54321" -e "FLUSH PRIVILEGES;"
# echo "All done."

mysqlsh userExample:54321@db/elyte --import data/valid_user.json users 

