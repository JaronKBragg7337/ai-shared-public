// Suits: the player in third person on Phobos (standing, walking, close front view), then Mars port people.
export default async ({ page, shot, ev, step, land }) => {
  await land('phobos');
  await ev(`stand(110,-20,Math.PI/2,-0.1,true)`);
  await step(30); await shot('s1-phobos-stand-back');
  // look at the player from the front, close: free camera 2.6 m ahead at chest height
  await ev(`cosmos.freeCam.showPlayer=true`);
  await ev(`cam([112.6,-20,1.5],[110,-20,1.1])`); await step(2); await shot('s2-phobos-front-close');
  await ev(`cam([110,-17.2,1.3],[110,-20,1.0])`); await step(2); await shot('s3-phobos-side');
  await ev(`cam([108.2,-21.8,1.9],[110,-20,1.1])`); await step(2); await shot('s4-phobos-back-quarter');
  await ev(`stand(110,-20,Math.PI/2,-0.1,true)`);
  await page.keyboard.down('KeyW'); await step(50); await shot('s5-phobos-walk-a'); await step(9); await shot('s6-phobos-walk-b'); await step(9); await shot('s7-phobos-walk-c'); await page.keyboard.up('KeyW');
};
