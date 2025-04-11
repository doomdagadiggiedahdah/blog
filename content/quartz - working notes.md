## 2025-04-10
- revamp my dang blog

### got it started
```

# getting started was easy 💙
# go here: https://quartz.jzhao.xyz/
# you'll find the git clone instructions

mktemp -d
/tmp/tmp.p0ZswtNYLk

git clone https://github.com/jackyzha0/quartz.git
nvm install 20 # fixes "unsupported engine"
npm i
npx quartz create
npx quartz build --serve --port 1323 # I have something on 8080 already, changed
# didn't need to add anything
# had a basic page that would open on localhost:1323
# I could edit the content/index.md, save, see changes in real time. nice feedback
```

### get first post
- wow, just pasted a post into content/other.md, the website autopopulated, I could click on it and view. It just worked.
- this is working pretty well I think. sweet.

### getting an mvp
- getting all my posts from current storage
	- I should be able to script this
- hooking up porkbun to github repo
- figuring out how to send all quartz posts to the github repo
- then we can try fucking with shit

### (break taken, picking up from first github commit)
- boom: https://github.com/doomdagadiggiedahdah/blog/commit/493968900ac4bb88b95355f88769f2ea9fc8b474
- nice. next is get the thing live and in front of me. I want to see instant changes of what I mess with.
- ok....I'm now at the point of being able to symlink...can I resolve quick?
	- copy folder. I create one with this document in it and that will be placed...in obsidian, fuck it


#### oof: split branches
- this needs to be synced to the actual one....
	- but then I can't write in obsidian....ugh. sloppy, but ok for now.

### get the website in front of me; serve it?
- hmm served it, no index.md file though. wait, what's happening? 
- beautiful. I went back to the og temp directory from first time `/tmp/tmp.p0ZswtNYLk`, copied file to current index.
- did it work? yes it did 🔥 push it 
- damn, this is cool. already got stuff online. this is a nice feedback loop to get into as well. kinda fun.

- ok, what next? I can see my changes in a local version of the website, endgoal is that my blog runs on this and doesn't die.
- need to have this be comfortable enough to where I can show people what I'm doing.
- need to host this. 
- before I host, I need to back up website as it is, maybe get some screen shots, (preserve the "work in progress",) and then I think this is github actions that pushes the code to porkbun? (I'm not clear on that last part). but for now, we back up old website. I think Claude can knock this out.
	- (later, clean out the old blog files in `/home/mat/Documents/blog-porkbun-hostg`)

### backing up ye old blog
- get the posts (in all their glory) first, and make sure it doesn't get deleted. (can save it in the github actually. do a once over to make sure you want to include all pieces.) `.archive`
- What's Claude suggest to do?
	- brief mention to a previous hacky script I put together; made a this script that created a knowledge graph of all your notes, uploaded your post to the ftp host, and then opened your posts in your browser to confirm that they uploaded as you expected them too.
	- it's cool looking back at old projects that were so hacky, but worked. it's cool to see the progress as well as the creativity.

```
> me
I can log into my hosting provider using this snippet:
'''
ftp -n -p $FTP_SERVER <<END_SCRIPT
user $FTP_USERNAME $FTP_PASSWORD
cd blog
put "$new_file"
ls
bye
END_SCRIPT
'''

but I would like to pull them. how do I do this?

```

- // realize I can already log in, where cr3eds?
- // from the creds file, duh `~/Documents/ProgramExperiments/.ftp_creds`

- `ftp -p $FTP_SERVER` (add the credentials) and great, I'm in. now let's look around `ls`

```
Name (pixie-ftp.porkbun.com:mat): enjoy.monster
331 User enjoy.monster OK. Password required
Password: 
230 OK. Current restricted directory is /
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Extended Passive mode OK (|||33693|)
150 Accepted data connection
drwxr-xr-x    2 501        nginx            6144 Nov 15 00:36 about
drwxr-xr-x    2 501        nginx            6144 Feb 18 07:33 assets
drwxr-xr-x    2 501        nginx            6144 Feb 18 09:01 blog
-rw-r--r--    1 501        nginx            3498 Nov 14 22:10 homepage.css
-rw-r--r--    1 501        nginx            2313 Nov 14 22:16 index.html
226-Options: -l 
226 5 matches total
ftp> 
```

- ok, got a few to copy back home. Claude gives everything we need:

'''
Use commands like:

`ls` to list files
`get` filename to download a file
`mget *.html` to download multiple files
`bye` or `quit` to exit
'''

- ok and after a bit of futzing I finally get my first download of something.

```
ftp> cd assets
250 OK. Current directory is /assets

ftp> get comb_of_commands.png
local: comb_of_commands.png remote: comb_of_commands.png
229 Extended Passive mode OK (|||33360|)
150-Accepted data connection
150 45.3 kbytes to download
100% |************************************************************************************************************************************************| 46355      573.92 KiB/s    00:00 ETA
226-File successfully transferred
226 0.008 seconds (measured here), 5.22 Mbytes per second
46355 bytes received in 00:00 (573.24 KiB/s)
ftp> bye
221-Goodbye. You uploaded 0 and downloaded 46 kbytes.
221 Logout.

## now to check that it downloaded, and where
mat@fantasyFlamingo:~/D/b/c/.archive$ ls
comb_of_commands.png # beauty
```

### cool, another milestone
- alright, got my first download. now let's get it all.


```
curl -u $FTP_USERNAME:$FTP_PASSWORD -l ftp://$FTP_SERVER/blog/assets/ | xargs -I {} curl -u $FTP_USERNAME:$FTP_PASSWORD ftp://$FTP_SERVER/{} -o {}
```
- let's push to github
