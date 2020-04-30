#!/bin/bash
rm -f ~/.ssh/id_rsa_blog*
echo $'-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAxSraxpJofj2Wy9rUSYfCCuK3fnLVGu+JabQ8/jbGhv17tj26\n3r8i37oAavp8Td8igcj13MJYFxJS2AtU7oWqpaajlQj4OR2NQKhGafnR111fNU4q\npsBqo8/2/ltJ3KksT12jVX+NkpKZR7zOUTGEbEbUWnWE0aTg4TzjYVaN+sHSyqN1\n1oMbNiH3kRkGzlUfH+hA9ow6yaJBrHnk6Z4/LPaucp25Ux2xnw9MMqLz8KqCqYO0\ntEUlL/kHev2DqAuiVk4z5VAnm2P/J2kIkdZEfRJg8qpY48Kw5Nj/Gtf+8W7U+GWk\n5gzEBHe2cDQ4XHijqgXwXInOinYoVYyhivA5WQIDAQABAoIBAQC1M4tYj1llG6ko\ntHYBFbkpU+8bUOG1HYuGD9U2NJUDnpZBiD3jVHnybvjPWGFBF96YtF3wgtN+cKKe\nVtu5UjLghmM0JsgphZU5ZO1BnAxUB0XmsW3VTmUzI391h+Q73WYRkpb3joBHwl8I\nZOagDAgNkpK6h+KG4SajGdhGrstRNYyD0R3AAjcO/162K2r6K/9HmQg6b50U+U7H\nN6j2x1KA6Wrfkdl2XaUSUe7pgBqK/Yk8gCV4PZMl/pNPUxCOMDvEDkVeqfclRD8A\nZ+K6GaAMIX2FKxwM2qOGcv3rig5ahkUjo6Q9qzVucgGLHnSiQK7Kmz1vU7wjm+D4\n7kJAOLIBAoGBAPyCjDETQ00+pl2hjFkhA549jes17gc6Ohz/YmADbNvK7U5SOUeL\n6GIeSF7iiCQ44yOr4SOM2jDArZZSR6ZwssQcxNC1HOkb5g2PtuBeZQIQanXB20Y2\nM0ZVRSBTi4EDfJ+5Edg/ucUh08NZKvHsqlbaOm1sGmp8yCmam42w+725AoGBAMfk\nfTyl8FXE/rwtv7qiR782oMGCmOHJ+9pyBLBwKtZSEGXk87qI/rz3oVcH1ed23eN5\niTn1zZDrF52tiHH0+nwF3Efaul1D9rz6ifGVbdVCRe6dGONln7xvd9VMRIBtHVnI\nsjNiWJfMWGl3c6M1/Jc2mCiF2QgpxByMI84TQSihAoGBALED97GDln+1Nr2WvaPR\n4A5zimTkppwMdqbTZax3Wj3u0VNBkwQUEXGPVx6lYdk6xAjCuo7IdEEPIeGqhq4o\nfTm8DUFeZgkI1MqXABXkNp0u0uMAZm6fGmzo5A/YYYis4BW8kMTvT5ThtOlSPifg\nyD0guSrySMZz+YIo73lyI9iJAoGAEmnM04phojT8Vi9Mqw+J1mZc1paGKL5ncc7w\n+aPLfmSe2BQIE5XNCXEyLoctQB4mAG9QocMvxXqyeTbkC8NKU6Rij0fpxO+eyfe2\nP0fJj0yEjp9wDHpvBXerLT3STZY/jua665rSmGEdf9GeGFm/w9ommA0EWgkm5I5Q\nOgpyBSECgYAZ25WuHiOJn5+dqFgSZnq6Ygyh6sUptjXVqavCLxjaGfXVt6uRonkw\nvfBYguUgavFViGBBgnCfEDZrwOBh4IpVzT2Ldn+qabFbWCZ11dDtFW5rXB4ulQbb\noYiIpeME9ejgHGPzTThukO5WQEJVfm3Fvxf478XkefQLKAW1O2Z/6w==\n-----END RSA PRIVATE KEY-----' >> ~/.ssh/id_rsa_blog
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDFKtrGkmh+PZbL2tRJh8IK4rd+ctUa74lptDz+NsaG/Xu2PbrevyLfugBq+nxN3yKByPXcwlgXElLYC1TuhaqlpqOVCPg5HY1AqEZp+dHXXV81TiqmwGqjz/b+W0ncqSxPXaNVf42SkplHvM5RMYRsRtRadYTRpODhPONhVo36wdLKo3XWgxs2IfeRGQbOVR8f6ED2jDrJokGseeTpnj8s9q5ynblTHbGfD0wyovPwqoKpg7S0RSUv+Qd6/YOoC6JWTjPlUCebY/8naQiR1kR9EmDyqljjwrDk2P8a1/7xbtT4ZaTmDMQEd7ZwNDhceKOqBfBcic6KdihVjKGK8DlZ root@ublog" >> ~/.ssh/id_rsa_blog.pub
echo "|1|dJASNxO/dHfoD2sAFDEnq/fGjGU=|IWuxf9GiudLECbItC354Yuywulw= ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBIrq3/9P0sJr0CtGxbCJa7GaPHWOSC+/0mweLuF+qslE7EzLW7Wl3dyVvXali6RQaBiOPL28Ip4tTc9zu5lirfg=" >>  ~/.ssh/known_hosts
chmod 400 ~/.ssh/id_rsa_blog
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade
sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" dist-upgrade
sudo apt-get install -y pwgen
if [ ! -f ~/databasepw ]; then
  databasepw=$(pwgen 13 1)
  echo $databasepw >> ~/databasepw
else
  databasepw=$(cat ~/databasepw)
fi
if [ ! -f ~/blogdbpw ]; then
  blogdbpw=$(pwgen 13 1)
  echo $blogdbpw >> ~/blogdbpw
else
  blogdbpw=$(cat ~/blogdbpw)
fi
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password password $databasepw"
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $databasepw"
sudo apt-get install -y uwsgi uwsgi-plugin-python git nginx unzip mercurial python-pip build-essential libssl-dev libffi-dev python-dev python3-dev openssh-server python-mysqldb mysql-server libmysqlclient-dev mysql-client
pip install --upgrade pip
cd /tmp
if [ ! -f /tmp/uweb3.zip ]; then
  rm uweb3.zip
fi
sed -i.bak -e 's/# server_names_hash_bucket_size 64/server_names_hash_bucket_size 128/g' /etc/nginx/nginx.conf
wget https://download.underdark.nl/public/uweb3.zip
unzip uweb3.zip -d /tmp
cd /tmp/uweb3
python setup.py install
rm -r /tmp/uweb3
mkdir /var/log/underdark/
chmod 775 /var/log/underdark/
chown www-data:www-data /var/log/underdark/
mkdir -p /opt/underdark/
cd /opt/underdark/
cp -r /home/sjoerdserv/ublog /opt/underdark/ublog
chmod -R 755 /opt/underdark
cd /opt/underdark/ublog
python setup.py install
mysql --user="root" --password="$databasepw" --execute="CREATE DATABASE blog DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;"
mysql --user="root" --password="$databasepw" --execute="GRANT ALL ON blog.* TO 'blog'@'localhost' IDENTIFIED BY '$blogdbpw';"
mysql --user="root" --password="$databasepw" blog < /opt/underdark/ublog/blog/schema/blog.sql
mkdir /var/www/blog
cd /var/www/blog
cp -r /opt/underdark/ublog /var/www/blog/application
mkdir logs
mkdir python_egg
mkdir static
cd static
ln -s ../application/blog/static/styles styles
sed -i.bak -e "s/password = pass/password = $blogdbpw/g" /var/www/blog/application/blog/config.ini
echo $'server {\n        listen          80;\n        server_name     $hostname;\n        access_log /var/www/blog/logs/access.log;\n        error_log /var/www/blog/logs/error.log;\n\n        location / {\n            uwsgi_pass      unix:///run/uwsgi/app/blog/blog.socket;\n            include         uwsgi_params;\n            uwsgi_param     UWSGI_SCHEME $scheme;\n            uwsgi_param     SERVER_SOFTWARE    nginx/$nginx_version;\n\n        }\n\n        location /styles {\n            root   /var/www/blog/static/;\n        }\n}' > /etc/nginx/sites-available/blog
echo $'<uwsgi>\n    <plugin>python</plugin>\n    <socket>/run/uwsgi/app/blog/blog.socket</socket>\n    <pythonpath>/var/www/blog/application/</pythonpath>\n    <chdir>/var/www/blog/application/</chdir>\n    <wsgi-file>ublog.wsgi</wsgi-file>\n    <master/>\n    <processes>4</processes>\n    <harakiri>60</harakiri>\n    <reload-mercy>8</reload-mercy>\n    <cpu-affinity>1</cpu-affinity>\n    <stats>/tmp/stats.socket</stats>\n    <max-requests>2000</max-requests>\n    <limit-as>512</limit-as>\n    <reload-on-as>256</reload-on-as>\n    <reload-on-rss>192</reload-on-rss>\n    <no-orphans/>\n    <vacuum/>\n</uwsgi>' > /etc/uwsgi/apps-available/blog.xml
ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/blog
ln -s /etc/uwsgi/apps-available/blog.xml /etc/uwsgi/apps-enabled/blog.xml
rm /etc/nginx/sites-enabled/default
chown -R www-data:www-data /var/www
chown -R root /var/www/blog/application/.hg
sudo pip install python-creole
service uwsgi restart
service nginx restart
