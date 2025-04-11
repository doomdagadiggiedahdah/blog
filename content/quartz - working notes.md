---
date_creation: 2025-04-10
time_creation: 15:46:58
tags:
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
	- but then I can't write in obsidian....ugh.
