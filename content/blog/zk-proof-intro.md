---
title: Quick Thoughts on ZK Proof Foundations
---

<center> ~~ A friendly exploration of zero-knowledge proof basics through dialogue ~~ </center>

# Intro

I like holding hands. This is a hand-holding post on the basic ideas of what makes **zero-knowledge proofs** work.

# Dialogue

**Person A:** So like, what are they?

**Person B:** Zero knowledge proof (ZKP), it's a way to convince another person that something is true, but you don't need to show proof of it (or to have "zero knowledge" of what makes something true).

**Person A:** What?

**Person B:** Yeah I know.

**Person A:** But how?

**Person B:** Well to start, I think that (with ZKP's) saying that "I have **proof** this is true!" is actually a bad word to use. We don't have proof! Instead, it's better to say "this thing is *probably* true".

**Person A:** ......

> ⚠️ **Key Concept**  
> Zero-knowledge proofs are about probability, not absolute certainty.

**Person B:** Quick background; there's two people in this equation, a prover (the one saying "believe me!") and the verifier (the one saying, "but how do I actually know?"). The prover wants the verifier to believe them, but doesn't want to give out some type of information. (let's just say the prover doesn't want to share their birthdate, but wants to go a club; **they need to prove that they're over 21**.)

**Person A:** Ok, prover needs to prove that they're over 21, but doesn't want to show their birthday.

**Person B:** Yup. Keep in mind that your proof will either equal "true or false" (like, you're over 21 or not)

**Person A:** Great

**Person B:** Great

**Person A:** But wait, proof = true or false, but you said it's better to say "probably true"?

**Person B:** Ya, so what happens with some fancy computer magic is the verifier (the one saying "can I actually believe the prover?") will give a bunch of True/False tests to the prover. These tests basically say (in computer terms) "ok, if you actually were over 21, then you should pass *this random test*!" The prover can now 1. either guess correctly each time (which sounds hard to do maybe), or they 2. actually are over 21 and you can pass the test.

**Person A:** But wouldn't the answer just be "yes" each time? That seems pretty easy to hack

**Person B:** Yeah that would, so they change it up a bit. But basically, if you have the ground truth, that you are over 21, it's easy to answer correctly. If you don't, you just have to guess. You have to guess right *every time they ask you a question*

**Person A:** 😲😯😮

**Person B:** ‼️🤯😵

**Person A:** Each time?

**Person B:** Ya, imagine having to guess correctly a whole bunch of times, and if you mess up once, *you're done kiddo*. And these guys like math, here's how you calculate the probability:

> 📊 **The Math of Certainty**  
> With each additional test, the probability of successfully guessing drops dramatically:
> - 1 test: 50% chance of guessing correctly
> - 2 tests: 25% chance
> - 3 tests: 12.5% chance
> - And so on...

**Person A:** Oh my

**Person B:** And this is also where "probably true" comes in. If someone guessed it right once, that's only 50% chance (true/false). But what if they had to get it right twice? That's 25% (50% x 50%). Three times? 12.5%.

**Person A:** And it just keeps going down?

**Person B:** Yup, put into your calculator (1/2)^{the number of tests you'd give}. (first try the above numbers, noting that you have to move the decimal two places to the right to get percentages like above. (1/2)^1 = .5 , but move it two and you've got 50%)

## Intermission!!

**You should actually plug some numbers** into the calculator to see how quickly the number goes down. Ask yourself this, if you were the verifier, what would your acceptable percentage be? How small of a chance would you accept of some rando correctly guessing each of your tests? How small does it have to be to accept that guessing correctly probably didn't happen?

## Back to the show

**Person A:** Wow, ten tests gives a 0.0976562% of someone guessing correctly, or 1/1024 chance of getting it right.

**Person B:** Crazy right!? And now again imagine yourself as the verifier (the person checking IDs). At what percentage do you say that you're convinced? Is a 9% possibility that a person is lying an "acceptable risk to take? The actual percentage is something fun to think about, but the more important thing is to realize that ***the verifier actually never sees the evidence of whether or not someone is lying, but instead the verifier sees a low enough probability that they're not lying*** and then they ***are convinced*** that there's no lying taking place. And also, if you're not satisfied, you can just ask for more tests (it just takes a bit longer for the calculations to be checked).

**Person A:** Ohhhhh

> 💡 **The Zero-Knowledge Part**  
> The verifier becomes *convinced* without ever seeing the actual proof or private information!

**Person B:** Yeahhhhhhh. And just to wrap it up: the verifier never actually **knows** that the prover is telling the truth (this *is* a **zero knowledge** proof). The verifier is just *convinced* at some point that the prover is telling the truth.
