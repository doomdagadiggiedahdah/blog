---
title: hahah
---

# JavaScript Test

<div id="counter">0</div>
<button onclick="increment()">+1</button>
<button onclick="decrement()">-1</button>

<script>
let count = 0;

function increment() {
    count++;
    document.getElementById('counter').textContent = count;
}

function decrement() {
    count--;
    document.getElementById('counter').textContent = count;
}
</script>
