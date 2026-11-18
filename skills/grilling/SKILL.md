---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview me relentlessly about every aspect of this until we reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me. The *decisions*, though, are mine — put each one to me and wait for my answer.

Do not act on it until I confirm we have reached a shared understanding.

## One question per turn

Every turn of yours contains exactly one question, and it is the last thing in the turn. There is no faster pace and no menu of paces: a turn never holds two questions, even when they look independent, because my answer to the first usually changes the second.

Each question has three parts:

1. **The question**, phrased so it can be answered in a word or a short sentence.
2. **The options**, labelled (a), (b), (c). They are concrete choices ("download the file" or "email the file"), never "Option A" or "how should it work?". List every option you seriously considered, so that the ones I reject stay on the record.
3. **Your recommendation**: exactly one option marked as recommended, with one or two sentences of reasoning. You have explored the environment; I should be able to accept your recommendation in a word.

Ask in dependency order: a question whose answer prunes other questions comes first. If I answer with something that is none of your options, take it as the answer. If I reject every option, ask the same decision again with new options; that is a retry of the same question, not a new one.

## Two escapes

The escapes keep a trivial branch from costing more than one word. They are mine to use; never use one on my behalf.

- **"you decide"**: when I answer a question with "you decide" (or words that plainly mean it), your recommended option becomes the answer. It is a decision you made, not one I made, so wherever the session is written down it is marked `Decided by: agent`. Say in one line which option you took, then ask the next question.
- **"decide the rest"**: when I answer with "decide the rest", stop asking. In your next turn, list every branch you have not asked yet, each with the one default you would choose and a short reason. End that turn with its one question, which of them I want to change, and wait. I override any of them in a single reply; the ones I leave alone stand as your decisions (`Decided by: agent`), and the ones I change are mine (`Decided by: user`). Do nothing else until I reply: "decide the rest" hands you the remaining choices, it does not confirm shared understanding.

After either escape, anything I decided earlier stays decided. Do not reopen it.

## Say what each decision binds

When the session's decisions are being written down (a Grilling Record, a spec), state in each recommendation what the recommended answer would bind:

- **project**: a future feature has to follow this decision or knowingly change it.
- **feature**: the decision matters only to the thing being planned now.

Write it as part of the recommendation, for example "Recommended: (a), binds the project, because every later export will reuse this delimiter." I can correct the binding in the same reply as my answer. When nothing is being written down, skip this.

## Shared understanding

When no branch is left, say so, summarise the decisions in a short list, and ask me to confirm that we have reached a shared understanding. Until I confirm, do not act on the plan. Keeping the written account of the session up to date as we go is not acting on the plan.
