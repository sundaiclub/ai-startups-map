# AI StartUps Map

#SetUp on a Google Cloud VM
On a fresh Debian server, run the following commands:

```bash
sudo apt install git
git clone https://github.com/sundaiclub/ai-startups-map.git
```

```bash
sudo apt install postgresql
sudo apt install -y postgresql-common
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
sudo apt-get install postgresql-15-pgvector
sudo systemctl start postgresql
```

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh 
./Miniconda3-latest-Linux-x86_64.sh 
source ~/.bashrc
```

```bash
cd ai-startups-map
conda create -n main python=3.9
conda activate main
pip install -r requirements.txt 
conda install pytorch-cpu
```

```bash
sudo systemctl start postgresql
sudo -i -u postgres
```

In the postgres shell, create a new user and database

```bash
CREATE USER postgres WITH PASSWORD 'postgres';
```

Index the data
```bash
python indexer.py
```

# Setup The NGinX Server
```bash
sudo apt-get install nginx python3-certbot-nginx certbot
sudo vim /etc/nginx/sites-available/ai-startups-map-backend.sundai.club
sudo ln -s /etc/nginx/sites-{available,enabled}/ai-startups-map-backend.sundai.club 
sudo systemctl restart nginx
sudo systemctl status nginx
```

```bash
sudo certbot --nginx
streamlit run app.py
```