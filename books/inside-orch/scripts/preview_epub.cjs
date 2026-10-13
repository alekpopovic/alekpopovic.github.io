/* Preview extracted final EPUB XHTML in Chromium; no reader-engine equivalence claimed. */
const {chromium}=require('@playwright/test');
const {spawnSync}=require('child_process');
const fs=require('fs'); const path=require('path'); const crypto=require('crypto');
(async()=>{
 const book=path.resolve(__dirname,'..'),epub=path.join(book,'dist/inside-orch.epub');
 const root=process.argv[2]; if(!root)throw new Error('Pass exact locally extracted EPUB directory.');
 const started=new Date().toISOString(),hash=crypto.createHash('sha256').update(fs.readFileSync(epub)).digest('hex');
 const integrity=spawnSync('python3',['-c',`import pathlib,zipfile,sys,json,xml.etree.ElementTree as ET
r=pathlib.Path(sys.argv[1]);z=zipfile.ZipFile(sys.argv[2]);bad=[n for n in z.namelist() if not n.endswith('/') and ((not (r/n).is_file()) or (r/n).read_bytes()!=z.read(n))]
if bad: raise SystemExit('Extraction differs from current EPUB: '+repr(bad))
texts=[n for n in z.namelist() if n.endswith('.xhtml')];footnotes=0
for n in texts:
 x=ET.fromstring(z.read(n));footnotes+=sum(1 for e in x.iter() if 'footnote' in str(e.attrib.get('{http://www.idpf.org/2007/ops}type','')))
print(json.dumps({'archive_members_byte_equal':True,'archive_members':len(z.namelist()),'xhtml_documents':len(texts),'footnote_markup_count':footnotes}))`,root,epub],{encoding:'utf8'});
 if(integrity.status!==0)throw new Error(integrity.stderr||integrity.stdout);
 const extractionIntegrity=JSON.parse(integrity.stdout);

 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||'/opt/google/chrome/chrome',args:['--no-sandbox']});
 const evidence={extraction_integrity:extractionIntegrity,epub_sha256:hash,started_at_utc:started,command:process.argv,working_directory:process.cwd(),browser_version:browser.version(),preview_engine:'Actual Chromium file:// rendering of unmodified extracted EPUB XHTML; reader-type preference simulated by font-size override, OS theme by prefers-color-scheme.',cases:[],navigation:[],failures:[],network_requests:[],screenshots_root:path.join(root,'screenshots')};
 fs.mkdirSync(evidence.screenshots_root,{recursive:true});
 const textDir=path.join(root,'EPUB/text'),find=prefix=>fs.readdirSync(textDir).find(n=>n.startsWith(prefix)&&n.endsWith('.xhtml'));
 const samples=[['chapter04','04-'],['chapter17','17-'],['appendixA','a-cli'],['appendixB','b-lifecycle'],['appendixC','c-annotated'],['appendixF','f-gloss']];
 const page=await browser.newPage();await page.route(/^https?:/,route=>{evidence.network_requests.push(route.request().url());return route.abort();});
 for(const scenario of [{id:'small-light',width:390,height:844,size:16,color:'light'},{id:'small-large-dark',width:390,height:844,size:24,color:'dark'},{id:'wide-light',width:1280,height:900,size:16,color:'light'},{id:'wide-large-dark',width:1280,height:900,size:24,color:'dark'}]){
  await page.setViewportSize({width:scenario.width,height:scenario.height});await page.emulateMedia({colorScheme:scenario.color,reducedMotion:'reduce'});
  for(const [label,prefix] of samples){
   const file=find(prefix);if(!file)throw new Error('Missing sample '+prefix);
   await page.goto('file://'+path.join(textDir,file));await page.addStyleTag({content:`body{font-size:${scenario.size}px !important}`});
   await page.locator('body').waitFor();
   const result=await page.evaluate(()=>({title:document.querySelector('h1')?.textContent,viewport:innerWidth,documentWidth:document.documentElement.scrollWidth,bodyFont:getComputedStyle(document.body).fontSize,bodyColor:getComputedStyle(document.body).color,background:getComputedStyle(document.body).backgroundColor,codeBlocks:document.querySelectorAll('pre').length,tables:document.querySelectorAll('table').length,images:[...document.images].map(i=>({src:i.getAttribute('src'),loaded:i.complete&&i.naturalWidth>0,alt:i.alt})),wideElements:[...document.querySelectorAll('pre,table,img')].filter(e=>e.getBoundingClientRect().right>innerWidth+2).map(e=>({tag:e.tagName,width:e.getBoundingClientRect().width,right:e.getBoundingClientRect().right}))}));
   const screen=path.join(evidence.screenshots_root,`${scenario.id}-${label}.png`);await page.screenshot({path:screen,fullPage:false});
   evidence.cases.push({scenario,...result,file:'EPUB/text/'+file,screenshot:screen,screenshot_sha256:crypto.createHash('sha256').update(fs.readFileSync(screen)).digest('hex')});
   if(result.documentWidth>result.viewport+2)evidence.failures.push(scenario.id+':'+label+':page overflow');
   if(result.images.some(i=>!i.loaded))evidence.failures.push(scenario.id+':'+label+':unloaded image');
   if(result.codeBlocks){const pre=page.locator('pre').first();await pre.scrollIntoViewIfNeeded();const codeScreen=path.join(evidence.screenshots_root,`${scenario.id}-${label}-code.png`);await page.screenshot({path:codeScreen});evidence.cases.at(-1).code_screenshot=codeScreen;}
   if(label==='appendixC'){await page.locator('pre').last().scrollIntoViewIfNeeded();const urlScreen=path.join(evidence.screenshots_root,`${scenario.id}-appendixC-long-url.png`);await page.screenshot({path:urlScreen});evidence.cases.at(-1).long_url_screenshot=urlScreen;}
   if(result.tables){const table=page.locator('table').first();await table.scrollIntoViewIfNeeded();const tableScreen=path.join(evidence.screenshots_root,`${scenario.id}-${label}-table.png`);await page.screenshot({path:tableScreen});evidence.cases.at(-1).table_screenshot=tableScreen;}
   if(label==='chapter04'){
    const diagram=page.locator('img').first();await diagram.scrollIntoViewIfNeeded();const dest=path.join(evidence.screenshots_root,`${scenario.id}-chapter04-diagram.png`);await page.screenshot({path:dest});evidence.cases.at(-1).diagram_screenshot=dest;
   }
  }
 }
 await page.goto('file://'+path.join(root,'EPUB/nav.xhtml'));const links=await page.locator('nav a').count();await page.locator('a[href*="04-domain"]').click();evidence.navigation.push({action:'Click contents Chapter 4',url:page.url(),h1:await page.locator('h1').textContent(),passed:page.url().includes('04-domain'),contents_entries:links});
 const answer=page.locator('a[href*="solutions-ch04-md.xhtml"]');await answer.first().click();evidence.navigation.push({action:'Follow Chapter 4 worked answers',url:page.url(),h1:await page.locator('h1').textContent(),passed:page.url().includes('ch04')});
 const back=page.locator('a[href*="04-domain"]');await back.first().click();evidence.navigation.push({action:'Return from answers to Chapter 4',url:page.url(),passed:page.url().includes('04-domain')});
 await page.goto('file://'+path.join(textDir,'cover.xhtml'));const cover=path.join(evidence.screenshots_root,'cover.png');await page.screenshot({path:cover,fullPage:true});evidence.cover={screenshot:cover,source:'EPUB/media/cover.png'};
 evidence.finished_at_utc=new Date().toISOString();evidence.overall_status=evidence.failures.length?'failed':'passed';evidence.preview_limitations=['Chromium XHTML preview is not Kindle, Apple Books, Kobo, Calibre or a dedicated EPUB engine.','Font-size override simulates user-selected type size; pagination and proprietary reading controls were not tested.','Footnote inspection applies only if the edition actually contains footnote markup.','Element overflow and screenshots remain explicit observations; structural EPUBCheck is a separate root-owned validation.'];
 fs.writeFileSync(path.join(book,'validation/publication/epub-reading-preview.json'),JSON.stringify(evidence,null,2)+'\n');await browser.close();console.log(JSON.stringify({hash,cases:evidence.cases.length,failures:evidence.failures,wide:evidence.cases.filter(c=>c.documentWidth>c.viewport+2).map(c=>({scenario:c.scenario.id,file:c.file,width:c.documentWidth,viewport:c.viewport})),navigation:evidence.navigation}));
})().catch(err=>{console.error(err);process.exit(1)});
