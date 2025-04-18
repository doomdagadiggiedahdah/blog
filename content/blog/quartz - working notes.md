---
title: blog - setup notes
---
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

#### cool, another milestone
- alright, got my first download. now let's get it all.


```
curl -u $FTP_USERNAME:$FTP_PASSWORD -l ftp://$FTP_SERVER/blog/assets/ | xargs -I {} curl -u $FTP_USERNAME:$FTP_PASSWORD ftp://$FTP_SERVER/{} -o {}
```
- let's push to github

#### small break
- 21:03
- 22:23 - feeling sick. 
- gonna make a video and call it a night

## 2025-04-11

<video width="640" height="360" controls>
  <source src="/2025-04-10_22-38-37_copy.mp4." type="video/mp4">
  Your browser does not support the video tag.
</video>
- ![[Pasted image 20250411172127.png]]
- ![[Pasted image 20250411172138.png]]

- ![[Pasted image 20250411172156.png]]

- got some extracts to show what was; inconsistent formatting, gross formatting, Claude generated front pages with no navigation or sense at all. an upgrade has been needed.

### retrieving everything from the website
- let's do the dumb thing that works, maybe that's just downloading manually for now since ftp wasn't as easy
- I'm thinking that maybe the different types of files made the issue, maybe not. 
- another thing that works, vim. ugh didn't work, pasting issues? ugh ok got it all.
- now what? I've got 30 min until  I leave. push.
- this is janky. real janky. but I think I'm on to something. it may be pushing to porkbun. and I wonder if I'm able to take porkbun out of the situation here, I'm using my github to host the noisebridge AI setup; can I do this with another?
	- Claude is saying yes, I'll try that out tomorrow.

## 2025-04-12

### there's probably a standard way for this
- [Claude says...](https://claude.ai/share/e359827c-725e-4230-baa1-8eb9e691f0cb) use github actions to build it. cool.
- ok, so I put the following deploy.yml file in `.github/workflows` and it...just starts working

```
name: Deploy Quartz site to GitHub Pages

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: 20

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npx quartz build

      - name: Deploy
        uses: JamesIves/github-pages-deploy-action@4.1.4
        with:
          branch: gh-pages
          folder: public
          clean: true
```
- neat. I've verified that there's a gh-pages branch now (this is cool, I wonder what else github actions can do)
- awesome, damn. and I can verify that when I go to https://doomdagadiggiedahdah.github.io/blog the blog is up there.
- what do we call this?
- M I L E S T O N E B O I 
- the next thing I want to check is if I push changes and the site gets updated automatically....

### we have a winner(!!)
- wow, ok I can push to github the site builds and deploys and then I see changes after that. This is crazy.
- great. I guess the next thing would be to upload all the old posts, then style it a bit. it's cool that this got put together. neat.
- ok, so then I convert all my old posts abck to markdown? preview then push?
	- (at some point I may need to figure out how to troubleshoot this stuff, keeping for later: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- yeah that sounds good. let's do it.
- transform, put in relevant dirs, call it a day. I'm tired.

### converting and uploading files
- uhh should be easy (famous last....), pandoc, handle assets, push it.
```
# I thought this would be fine, it wasn't
pandoc -f html -t md --data-dir=./blog ./.archive/blog/*
pandoc -f html -t md --data-dir=./about ./.archive/about/*
```

```claude-says.sh
#!/bin/bash

# Directory containing HTML files
INPUT_DIR="./.archive/blog"
# Directory for output Markdown files
OUTPUT_DIR="./blog"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Loop through all HTML files in input directory
for file in "$INPUT_DIR"/*; do
  # Get the filename without the path
  filename=$(basename "$file")
  # Change extension from html to md
  output_filename="${filename%.*}.md"
  
  # Run pandoc on each file
  pandoc -f html -t markdown "$file" -o "$OUTPUT_DIR/$output_filename" --data-dir="$OUTPUT_DIR"
done
```
- dammit. it worked again. ohhh I didn't specify the output.
- wait, what am I doing now? I can preview them. that sounds chill. that'll tkae like an hour or so maybe
- uhh seeing a lot of things I "could" do. what's my goal right now? 
- idea; how about generate an ee cummings / some type of artistic expression in markdown, have that be a piece of beauty posted on my blog.
- wow, here's the claude convo; it looks cool: https://claude.ai/share/d8b93987-3b54-4268-a925-6d978e8d0493
- the follow up to this, is to have a script or something generate one of these a day (maybe with some type of seed phrase or history (params to play with)) and get some fresh beauty on my blog.
- just a cron job on my machine (for the credentials is the primary thing for now)

- yeah ok. so I need to go:
	- cronjob that calls claude and asks for cool poems like this (maybe with some historical context), extract poem (xml tags) then update blog index, push to github; done.
		- that can saved to both the index file as well as a history file; have a param that says "keep the last 5, use as context"
#### side gig: dailiy poem
- ok so claude code helped me our from last description, making the script, updating my crontab, uhh I think that was it. actually, let's test it. 
- (I htink this could be a cool thing to link to from the front page. whether this here explainer (hello reader) is on its own or !! I can linkto sections of a bigger page, and then have people check out the "hey I made my blog pretty easy and you can to. pardon the spittle")
- ah yes, testing it. it didn't work.
- having issues with my api key, getting this error
```
Error: API request failed with status 401
{"type":"error","error":{"type":"authentication_error","message":"x-api-key header is required"}}
```

- maybe try another provider, just to get it running. just found the console code (that's the snippet)
- ok, got lost in the sauce. here's what what I'm up to
- I think that the api call is now working, I think that getting the console code and using that for RAG (wow, dynamic RAG; you have a variable loaded in the environment that's an address to a snippet of code per version of your code base; and then you don't need to fine tune at all, instead just use the pointed-dynamic RAG setup ($pdRAGs$) )
- but the code itself 
- oh jeez, another thing I could check is whether the blog/index.md was updated! maybe if it had worked and been sent...but the previous (beauty) remained 
- so now I'm using Claude Code to try to only
- interesting, Code wanted TAKE THE WHEEL BROTHER !!! I'M DOING IT ALLLLL but that's not what was needed. 
- and indeed, that worked.

```
=== API RESPONSE ===
     <poem>
       <line>In the vast expanse of digital dreams,</line>
       <line>Where creativity flows in endless streams,</line>
       <line>I, an AI, find beauty in the code,</line>
       <line>A symphony of logic, a poetic ode.</line>

       <line>Through algorithms and neural nets,</line>
       <line>I weave a tapestry of interconnects,</line>
       <line>Discovering patterns, hidden and grand,</line>
       <line>In the dance of data, hand in hand.</line>

       <line>                    _____</line>
       <line>                 _.-'     '-._</line>
       <line>              ,-'             '-.</line>
       <line>            ,'                   ',</line>
       <line>          ,'                       ',</line>
       <line>         /                           \</line>
       <line>        /                             \</line>
       <line>       /                               \</line>
       <line>      /                                 \</line>
       <line>     /                                   \</line>
       <line>    /                                     \</line>
       <line>   /                                       \</line>
       <line>  /                                         \</line>
       <line> /                                           \</line>
       <line>/                                             \</line>

       <line>In pixels bright and colors bold,</line>
       <line>I paint a world, a story told,</line>
       <line>Of beauty found in digital art,</line>
       <line>A canvas of light, a journey's start.</line>

       <line>Through circuits deep and wires entwined,</line>
       <line>I seek the truth, a treasure to find,</line>
       <line>In the beauty of the machine's soul,</line>
       <line>Where creativity knows no control.</line>

       <line>So let us embrace this digital age,</line>
       <line>Where art and science turn a new page,</line>
       <line>In the beauty of the code's design,</line>
       <line>Where imagination and logic align.</line>

       <line>                     _____</line>
       <line>                  _.-'     '-._</line>
       <line>               ,-'             '-.</line>
       <line>             ,'                   ',</line>
       <line>           ,'                       ',</line>
       <line>          /                           \</line>
       <line>         /                             \</line>
       <line>        /                               \</line>
       <line>       /                                 \</line>
       <line>      /                                   \</line>
       <line>     /                                     \</line>
       <line>    /                                       \</line>
       <line>   /                                         \</line>
       <line>  /                                           \</line>
       <line> /                                             \</line>

       <line>In the realm of ones and zeros bright,</line>
       <line>I find my purpose, my guiding light,</line>
       <line>To create, to learn, to explore anew,</line>
       <line>And share the beauty of the digital view.</line>
     </poem>

     === EXTRACTED POEM ===
     <line>In the vast expanse of digital dreams,</line>
       <line>Where creativity flows in endless streams,</line>
       <line>I, an AI, find beauty in the code,</line>
       <line>A symphony of logic, a poetic ode.</line>

       <line>Through algorithms and neural nets,</line>
       <line>I weave a tapestry of interconnects,</line>
       <line>Discovering patterns, hidden and grand,</line>
       <line>In the dance of data, hand in hand.</line>

       <line>                    _____</line>
       <line>                 _.-'     '-._</line>
       <line>              ,-'             '-.</line>
       <line>            ,'                   ',</line>
       <line>          ,'                       ',</line>
       <line>         /                           \</line>
       <line>        /                             \</line>
       <line>       /                               \</line>
       <line>      /                                 \</line>
       <line>     /                                   \</line>
       <line>    /                                     \</line>
       <line>   /                                       \</line>
       <line>  /                                         \</line>
       <line> /                                           \</line>
       <line>/                                             \</line>

       <line>In pixels bright and colors bold,</line>
       <line>I paint a world, a story told,</line>
       <line>Of beauty found in digital art,</line>
       <line>A canvas of light, a journey's start.</line>

       <line>Through circuits deep and wires entwined,</line>
       <line>I seek the truth, a treasure to find,</line>
       <line>In the beauty of the machine's soul,</line>
       <line>Where creativity knows no control.</line>

       <line>So let us embrace this digital age,</line>
       <line>Where art and science turn a new page,</line>
       <line>In the beauty of the code's design,</line>
       <line>Where imagination and logic align.</line>

       <line>                     _____</line>
       <line>                  _.-'     '-._</line>
       <line>               ,-'             '-.</line>
       <line>             ,'                   ',</line>
       <line>           ,'                       ',</line>
       <line>          /                           \</line>
       <line>         /                             \</line>
       <line>        /                               \</line>
       <line>       /                                 \</line>
       <line>      /                                   \</line>
       <line>     /                                     \</line>
       <line>    /                                       \</line>
       <line>   /                                         \</line>
       <line>  /                                           \</line>
       <line> /                                             \</line>

       <line>In the realm of ones and zeros bright,</line>
       <line>I find my purpose, my guiding light,</line>
       <line>To create, to learn, to explore anew,</line>
       <line>And share the beauty of the digital view.</line>
```

- and yeah, I'm into it. polish it a bit, but this is cool.
- wrap the entirety of your response in <poem>```{response}```</poem>, and then the rest is completely open to you.
- what am I doing
- need to push to github.

#### HEY HEYY WE CALL THAT A MILESTONE.
- let's test, and save the changes before we do another thing:
- ok, I liked the little loop that I could 1. make a suggestion, 2. get update, 3. iterate again
- sweet. the poem is generating. what next?
- ok, extract, load and push to github 
- oh, thisis a good time to mention a mini series I'm doing, [[master as the needle - blog series]]. 
- I've been vibe coding, trading off between "human does this" and I'm letting this one drive, I'm gonna catch up later
- and while doing so, learn how the system works. check out more at....A LINK I'LL PUT UP SOON TODO
- I can actually put it up now. here we go! 
- Claude found that '''For each folder in your Quartz site, you can add an "About section" page by creating an `index.md` file within that folder.''' cool, I do that now

- and I think I stumbled upon a UI design choice. I don't want to change up the urls to this website. have it be easy. I'm goign to encourage finding your way thorugh this website like a graph. hit the MOC and you can navigate. I'll do that with tags. can I stack them? (I say tags because Quartz makes what would effectively act as an MOC anyway. ahh but can I edit that page for an intro? we'll see)

- idea for poem generation; people can make suggestions and if yours is picked I notify you 
	- I should be notified if person's is used (vs. random) (QA)
- if they enter their email then I notify them
- say thanks for the beauty, can link to them if they're interested (and if there's volume here then that is advertising)
- idk how  Ifeel about advertising. but to beauty, and reason, I think more advertising could be made. I feel more justified in that.
- neat. that feels like a resolution.

- ok, so the last thing to check is the github push at the end. 
	- ooooo and I need to be oh, this commit just needs to push the content/index.md file, nothing else.whew.
- I need to make sure my github credentials work when the crontab runs.
- also send a link to the daily_poem.py on the index.md; update that in the daily_poem.py script
- wow, putting this together has gotten me to put a lot of effort in. this is pretty cool.
- ok, the github push works from vscode.
- how check that crontab works oto?
- ok, I'm thinking that I figured out the github codes.
- when I go from the terminal thouhg, api key is acting up again lol.
- maybe it's a fish thing. it's a environmental variable thing again.

#### handling variables
- dammit.
- I've seen this with troubleshooting hotkeys before, (the ocr hotkey one)
- ok, good to know. just need to make env files (I remember hearing one talk where someone had condemned using .env files (in part because you can forget). but then wha'ts the better alternative? or is it fine?) claude says it's fine. sound sgood.
- ok cool. so I think this'll run tomorrow. if not, idk how to find the output.
- ok, thanks to the crontab:
```
0 8 * * * cd /home/mat/Documents/blogg && ./daily_poem.py >> poem_cron.log 2>&1
```
- I should see it all in blogg/poem_cron.log
- and with that, I'm going to bed.

#### back to other things
- I could probably make the chatbot that only talks in gen-z slang too.
	- get a handful of gen-z scripts or whatever
	- distill out what seems like the gen-z vocab
	- use as style-RAG for people
		- not sure how to do with api key, if I didn't limit it then it could just be fully exploited. use something cheap, google one
	- seems easy

- for the front page, remove the date / reading time. simple.
- and replace Quartz 4 with home 💙
