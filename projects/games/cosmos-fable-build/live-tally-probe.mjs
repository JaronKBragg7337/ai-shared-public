// Does the LIVE game server know the tally runs and the count action? (11/23, after its restart on 6a863cfa.)
// A throwaway visitor at Marineris Port asks three things the server must refuse, each for a reason only the new code has. A refusal changes nothing on the
// server (the authority rolls the action back). A tally taken and paid on the live server needs a flight to a world with a yard: not done here.
export default async ({ page, log, H, shot, sleep }) => {
  log('me', await H.me());
  const rq = (a) => page.evaluate((x) => cosmos.world.request(x), a);
  log('1 a count with no job on        ->', await rq({ type: 'mission-count', n: 3 }));
  log('2 a Moon tally asked for on Mars ->', await rq({ type: 'mission-accept', id: 'moon-fr-tally-fortis' }));
  log('3 a job that does not exist      ->', await rq({ type: 'mission-accept', id: 'no-such-job' }));
  await sleep(500); await shot('probe');
};
