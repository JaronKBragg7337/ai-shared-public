// step 0: who am I on the live world, where, and what is on screen
export default async ({ shot, log, sleep, H }) => { log('me', await H.me()); log('buttons', await H.buttons()); await shot('start'); log('text', (await H.text()).slice(0, 500)); };
