import { createRequire } from 'node:module';
import { mkdirSync, writeFileSync } from 'node:fs';
import assert from 'node:assert/strict';
const require = createRequire('C:/Users/lilli/.codex/runtime/unfinished-island/node_modules/');
const { chromium } = require('playwright');
const base = process.argv[2] || 'http://127.0.0.1:8767';
const local = base.includes('127.0.0.1');
const out = `C:/Users/lilli/AI-Shared/agents/astra/worlds-qa/${local ? 'local' : 'live'}`;
mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ headless: true, executablePath:'C:/Users/lilli/AppData/Local/ms-playwright/chromium-1234/chrome-win64/chrome.exe', args: ['--use-angle=d3d11'] });
const report = [];
try {
for (const mobile of [false, true]) {
  const context = await browser.newContext({ viewport: mobile ? { width:375,height:812 } : {width:1440,height:900}, hasTouch:mobile,isMobile:mobile,deviceScaleFactor:1 });
  const page = await context.newPage();
  page.setDefaultTimeout(30000);
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  if (local) await page.route('**/engine/hub/main.js?*', async route => {
    const res = await route.fetch();
    await route.fulfill({response:res,body:await res.text() + '\nwindow.hubQA = {state,camera,scene,npcs,characters,remotes,mindActors,renderCharacters,updateNpcs,look,updateDayNight, get held(){return viewmodel}, get sun(){return sunLight}};'});
  });
  console.log(`START ${mobile?'phone':'desktop'} hub`);
  await page.goto(base + '/engine/hub/', {waitUntil:'domcontentloaded',timeout:90000});
  await page.waitForFunction(() => document.querySelector('#fsButton'));
  if (mobile) await page.locator('#enterButton').tap(); else await page.locator('#enterButton').click();
  await page.waitForTimeout(1200);
  assert.equal(await page.evaluate(() => !!document.fullscreenElement),false);
  if (!mobile) {
    await page.keyboard.press('h');
    await page.waitForTimeout(400);
    if(local) {
      const held = await page.evaluate(() => ({parent:hubQA.held.parent===hubQA.camera,scale:hubQA.held.scale.x,z:hubQA.held.position.z}));
      assert(held.parent && held.scale<=.8 && held.z===-.85);
    }
    await page.screenshot({path:out+'/desktop-cup.png'});
    await page.keyboard.press('Escape');
    await page.waitForTimeout(200);
    const close=page.locator('#closeSettingsButton');
    if(await close.isVisible()) await close.click();
    await page.mouse.move(800,450); await page.mouse.down(); await page.mouse.move(850,480,{steps:10}); await page.mouse.up();
    await page.mouse.move(820,450); await page.mouse.down(); await page.mouse.move(770,420,{steps:10}); await page.mouse.up();
    assert.equal(await page.evaluate(()=>!!document.fullscreenElement),false);
    if(local) {
      assert(Math.abs(await page.evaluate(()=>hubQA.state.pitch))<.3);
      const before=await page.evaluate(()=>{hubQA.look(0,10000); return hubQA.state.pitch;});
      assert(Math.abs(before)<.3);
      const roster=await page.evaluate(()=>{
        hubQA.characters.clear();
        for(let i=0;i<20;i++) hubQA.characters.set('qa-'+String(i).padStart(6,'0'),{auth_user_id:'qa-'+String(i).padStart(6,'0'),display_name:i<3?'USER':'Resident '+i,presence:'away'});
        hubQA.renderCharacters(); hubQA.updateNpcs();
        const ns=[...hubQA.npcs.values()]; let min=Infinity;
        for(let i=0;i<ns.length;i++)for(let j=i+1;j<ns.length;j++)min=Math.min(min,ns[i].group.position.distanceTo(ns[j].group.position));
        return {min,names:ns.map(n=>n.name)};
      });
      assert(roster.min>=2.39,JSON.stringify(roster));
      assert.equal(new Set(roster.names).size,20);
      // Verify that two real minutes advance only 1/30 of the full sun orbit.
      const delta=await page.evaluate(()=>{const original=Date.now; const t=original(); Date.now=()=>t; hubQA.updateDayNight(0); const a=hubQA.sun.position.clone(); Date.now=()=>t+120000; hubQA.updateDayNight(0); const b=hubQA.sun.position.clone(); Date.now=original; return a.distanceTo(b);});
      assert(delta<10,`sun moved ${delta}`);
    }
  } else {
    await page.locator('#menuButton').tap();
    assert(await page.locator('#settingsPanel').isVisible());
    await page.locator('#closeSettingsButton').tap();
    const cdp=await context.newCDPSession(page);
    await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:280,y:400}]});
    await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:300,y:420}]});
    await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
  }
  await page.screenshot({path:out+`/${mobile?'phone':'desktop'}-hub.png`});
  report.push({world:'hub',mobile,errors:[...errors]});
  errors.length=0;
  console.log(`START ${mobile?'phone':'desktop'} Ashgrove`);
  await page.addInitScript(()=>{window.loadSamples=[];new MutationObserver(()=>{const p=document.querySelector('#load .bar');if(p)window.loadSamples.push({value:p.getAttribute('aria-valuenow'),text:document.getElementById('loadMsg')?.textContent});}).observe(document,{subtree:true,attributes:true,attributeFilter:['aria-valuenow']});});
  await page.goto(base+'/world3/',{waitUntil:'domcontentloaded',timeout:90000});
  await page.waitForFunction(()=>document.querySelector('#load')?.style.display==='none',{},{timeout:120000});
  assert.equal(await page.locator('#help').isVisible(),false);
  const data=await page.evaluate(()=>({samples:window.loadSamples,buildings:TOWN.Town.buildingCount,founding:TOWN.Town.buildings.filter(b=>!b.growth).length}));
  assert(data.samples.some(s=>Number(s.value)>0&&Number(s.value)<25));
  assert(data.samples.some(s=>Number(s.value)>46&&Number(s.value)<70));
  assert.equal(data.founding,49);
  await page.keyboard.press('g'); await page.keyboard.press('m'); await page.keyboard.press('t');
  assert.equal(await page.evaluate(()=>TOWN.Debug.on||TOWN.Edit.on),false);
  await page.keyboard.press('h');
  assert(await page.locator('#help').isVisible());
  const help=await page.locator('#help').innerText();
  assert(!help.includes('inspection layer')&&!help.includes('teleport box'));
  if(mobile) await page.locator('#bClose').tap(); else await page.locator('#bClose').click();
  await page.keyboard.press('j');
  const status=await page.locator('#town').innerText();
  assert(!status.includes('Awaiting validation'));
  assert(status.includes('founding buildings')&&status.includes('added since founding'));
  await page.screenshot({path:out+`/${mobile?'phone':'desktop'}-status.png`});
  if(mobile)await page.locator('#bTownClose').tap();else await page.locator('#bTownClose').click();
  const menu=page.getByRole('button',{name:'Menu',exact:true});
  if(mobile)await menu.tap();else await menu.click();
  await page.locator('#hbsDev').check();
  assert.equal(await page.evaluate(()=>document.body.classList.contains('dev')),true);
  await page.locator('#hbsDev').uncheck();
  await page.keyboard.press('Escape');
  await page.screenshot({path:out+`/${mobile?'phone':'desktop'}-ashgrove.png`});
  report.push({world:'ashgrove',mobile,errors:[...errors],...data});
  await page.goto(base+'/world3/gate/',{waitUntil:'domcontentloaded'});
  assert((await page.locator('body').innerText()).includes('49 founding buildings'));
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  await page.screenshot({path:out+`/${mobile?'phone':'desktop'}-gate.png`,fullPage:true});
  await page.getByRole('link',{name:'Enter Ashgrove'}).click();
  assert(new URL(page.url()).pathname==='/world3/');
  await context.close();
  console.log(`PASS ${mobile?'phone':'desktop'}`);
}
} finally {writeFileSync(out+'/report.json',JSON.stringify(report,null,2));await browser.close();}
console.log(JSON.stringify(report.map(({samples,...r})=>({...r,progressSamples:samples?.length})),null,2));
