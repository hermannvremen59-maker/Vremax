// Données de démonstration (fictives) pour captures d'écran
(function(){
const ENT='E1';
localStorage.setItem('vx_session',JSON.stringify({token:'demo',eid:ENT,enom:'Entreprise Démo',unom:'Direction',role:'admin',ident:'DEMO'}));
const C=[['101','Capital social',1],['110','Report à nouveau',1],['162','Emprunts auprès des établissements de crédit',1],['244','Matériel de bureau et informatique',2],['245','Matériel de transport',2],['284','Amortissements du matériel',2],['311','Marchandises',3],
['401','Fournisseurs',4],['401001','Fournisseur — Grossiste Alimentaire',4],['401002','Fournisseur — Transports Express',4],['401003','Fournisseur — Imprimerie Centrale',4],
['411','Clients',4],['411001','Client — Supermarché Étoile',4],['411002','Client — Hôtel Lagune',4],['411003','Client — Clinique Santé Plus',4],['411004','Client — Restaurant Le Baobab',4],
['421','Personnel, avances et acomptes',4],['431','Sécurité sociale',4],['443','État, TVA facturée',4],['445','État, TVA récupérable',4],['471','Comptes d’attente',4],
['512','Banques',5],['521','Banque',5],['531','Mobile Money',5],['571','Caisse',5],['585','Virements de fonds',5],
['601','Achats de marchandises',6],['604','Achats stockés de matières consommables',6],['605','Autres achats',6],['611','Transports sur achats',6],['622','Locations et charges locatives',6],['624','Entretien, réparations et maintenance',6],['627','Publicité et relations publiques',6],['628','Frais de télécommunications',6],['631','Frais bancaires',6],['641','Impôts et taxes directs',6],['661','Rémunérations directes versées au personnel',6],['664','Charges sociales',6],['671','Intérêts des emprunts',6],['681','Dotations aux amortissements d’exploitation',6],
['701','Ventes de marchandises',7],['706','Services vendus',7],['707','Produits accessoires',7]];
const COMPTES=C.map(c=>({entreprise_id:ENT,numero:c[0],intitule:c[1],classe:c[2]}));
const E=[],L=[]; let id=0; const seq={};
const today=new Date('2026-10-12T12:00:00');
function d(daysAgo){const x=new Date(today);x.setDate(x.getDate()-daysAgo);return x.toISOString().slice(0,10);}
function ecr(j,date,piece,lib,lignes,extra){id++;const eid='e'+id;const y=date.slice(0,4);seq[j+y]=(seq[j+y]||0)+1;
  E.push(Object.assign({id:eid,entreprise_id:ENT,journal_code:j,date_ecriture:date,piece,libelle:lib,statut:'valide',numero:j+'-'+y+'-'+String(seq[j+y]).padStart(5,'0'),utilisateur:'Direction',cree_le:date},extra||{}));
  lignes.forEach((l,i)=>L.push({id:eid+'_'+i,ecriture_id:eid,entreprise_id:ENT,compte_numero:l[0],libelle:l[1]||lib,debit:l[2]||0,credit:l[3]||0,lettrage:l[4]||null,axe:l[5]||null,pointee:!!l[6]}));}
const r=v=>Math.round(v);
// à-nouveaux
ecr('OD',d(345),'AN-2025','Apport en capital',[['521','Apport',15000000,0],['101','Capital',0,15000000]]);
ecr('BQ',d(330),'EMP-01','Emprunt bancaire',[['521','Emprunt',8000000,0],['162','Emprunt',0,8000000]]);
ecr('AC',d(320),'FA-0007','Achat véhicule de livraison',[['245','Véhicule',9500000,0],['521','Paiement',0,9500000]]);
ecr('AC',d(300),'FA-0012','Achat matériel informatique',[['244','Ordinateurs',1800000,0],['521','Paiement',0,1800000]]);
let n=1;
for(let m=11;m>=0;m--){
  const base=m*30+20; const g=1+(11-m)*0.045;
  for(let k=0;k<4;k++){const ttc=r((2100000+k*350000)*g*(0.92+((m*7+k*3)%5)*0.04)); const ht=r(ttc/1.18);
    const tr=k%3===0?'531':(k%3===1?'571':'521');
    ecr('VE',d(base-k*7),'VTE-'+String(n++).padStart(4,'0'),'Ventes comptoir',[[tr,'Encaissement',ttc,0],['701','Ventes HT',0,ht],['443','TVA facturée',0,ttc-ht]],null);}
  const cli=['411001','411002','411003','411004'][m%4]; const ttcC=r(1650000*g); const htC=r(ttcC/1.18);
  ecr('VE',d(base-3),'FAC-'+String(n++).padStart(4,'0'),'Facture client '+cli,[[cli,'Facture',ttcC,0,m>3?'LA'+m:null],['706','Prestation HT',0,htC,null,m%2?'Projet Riviera':'Projet Marcory'],['443','TVA',0,ttcC-htC]]);
  if(m>3) ecr('BQ',d(base-20),'RGL-'+m,'Règlement client '+cli,[['521','Encaissement',ttcC,0],[cli,'Règlement',0,ttcC,'LA'+m]]);
  const ach=r(5200000*g); const htA=r(ach/1.18); const fo=['401001','401002','401003'][m%3];
  ecr('AC',d(base-1),'FF-'+String(100+m),'Facture fournisseur '+fo,[['601','Achats marchandises',htA,0,null,m%2?'Projet Riviera':null],['445','TVA récupérable',ach-htA,0],[fo,'Dette fournisseur '+(fo==='401001'?'Grossiste Alimentaire':fo==='401002'?'Transports Express':'Imprimerie Centrale'),0,ach,m>2?'LF'+m:null]]);
  if(m>2) ecr('BQ',d(base-15),'REGL-'+m,'Règlement fournisseur',[[fo,'Règlement',ach,0,'LF'+m],['521','Paiement',0,ach]]);
  ecr('BQ',d(base-2),'LOY-'+m,'Loyer du local',[['622','Loyer',450000,0],['521','Virement',0,450000]]);
  ecr('OD',d(base-25),'SAL-'+m,'Salaires du mois',[['661','Salaires nets',1350000,0],['664','Charges sociales',215000,0],['521','Paiement',0,1565000]]);
  ecr('BQ',d(base-12),'TEL-'+m,'Internet et téléphone',[['628','Télécom',95000,0],['521','Prélèvement',0,95000]]);
  ecr('BQ',d(base-13),'BQ-'+m,'Frais bancaires',[['631','Frais',18500,0],['521','Prélèvement',0,18500]]);
  if(m%3===0) ecr('BQ',d(base-8),'PUB-'+m,'Campagne publicitaire',[['627','Publicité',320000,0],['521','Paiement',0,320000]]);
  if(m%2===0) ecr('CA',d(base-9),'ENT-'+m,'Entretien véhicule',[['624','Entretien',145000,0],['571','Espèces',0,145000]]);
  ecr('OD',d(base-10),'VIR-'+m,'Dépôt espèces en banque',[['521','Dépôt',1800000,0],['571','Dépôt',0,1800000]]);
}
// créances anciennes non réglées (+90 j)
ecr('VE',d(128),'FAC-0901','Facture client Hôtel Lagune',[['411002','Facture',2360000,0],['706','Prestation HT',0,2000000],['443','TVA',0,360000]]);
ecr('VE',d(104),'FAC-0915','Facture client Clinique Santé Plus',[['411003','Facture',1180000,0],['706','Prestation HT',0,1000000],['443','TVA',0,180000]]);
ecr('OD',d(60),'DOT-2026','Dotation amortissement — Véhicule',[['681','Dotation',1583333,0],['284','Amortissement',0,1583333]]);
ecr('BQ',d(30),'INT-01','Intérêts emprunt',[['671','Intérêts',185000,0],['521','Prélèvement',0,185000]]);
E.sort((a,b)=>b.date_ecriture.localeCompare(a.date_ecriture));
const BAL={}; L.forEach(l=>{const b=BAL[l.compte_numero]=BAL[l.compte_numero]||{entreprise_id:ENT,compte_numero:l.compte_numero,total_debit:0,total_credit:0,solde:0};b.total_debit+=l.debit;b.total_credit+=l.credit;b.solde=b.total_debit-b.total_credit;});
const TIERS=[['client','Supermarché Étoile','411001'],['client','Hôtel Lagune','411002'],['client','Clinique Santé Plus','411003'],['client','Restaurant Le Baobab','411004'],['fournisseur','Grossiste Alimentaire','401001'],['fournisseur','Transports Express','401002'],['fournisseur','Imprimerie Centrale','401003']].map((t,i)=>({id:'t'+i,entreprise_id:ENT,type:t[0],nom:t[1],compte:t[2],telephone:''}));
const DB={
 compta_comptes:COMPTES,
 compta_journaux:[['AC','Achats'],['VE','Ventes'],['BQ','Banque'],['CA','Caisse'],['OD','Opérations diverses']].map(j=>({entreprise_id:ENT,code:j[0],libelle:j[1]})),
 compta_ecritures:E, compta_lignes:L, compta_balance:Object.values(BAL),
 compta_params:[{entreprise_id:ENT,regime:'rsi',activite:'commerce',taux_tva:18,devise:'XOF',centre_impots:'CDI',mode_brouillard:false,verrou_jusqu_au:'2026-08-31',forme_juridique:'SARL'}],
 compta_exercices:[{id:'x1',entreprise_id:ENT,libelle:'Exercice 2026',date_debut:'2026-01-01',date_fin:'2026-12-31',statut:'ouvert'},{id:'x0',entreprise_id:ENT,libelle:'Exercice 2025',date_debut:'2025-01-01',date_fin:'2025-12-31',statut:'cloture'}],
 compta_immos:[{id:'i1',entreprise_id:ENT,libelle:'Véhicule de livraison',valeur:9500000,duree_annees:5,compte_immo:'245',compte_amort:'284',date_acquisition:d(320),amorti_cumule:1583333,cree_le:d(320)},{id:'i2',entreprise_id:ENT,libelle:'Matériel informatique',valeur:1800000,duree_annees:3,compte_immo:'244',compte_amort:'284',date_acquisition:d(300),amorti_cumule:0,cree_le:d(300)}],
 compta_tiers:TIERS,
 compta_budgets:[{id:'b1',entreprise_id:ENT,annee:2026,compte_prefix:'60',libelle:'Achats',montant:68000000},{id:'b2',entreprise_id:ENT,annee:2026,compte_prefix:'66',libelle:'Masse salariale',montant:24000000},{id:'b3',entreprise_id:ENT,annee:2026,compte_prefix:'62',libelle:'Services extérieurs',montant:9800000},{id:'b4',entreprise_id:ENT,annee:2026,compte_prefix:'70',libelle:'Ventes',montant:150000000}],
 ventes:(function(){const v=[];for(let i=0;i<9;i++){const dd=d(i+1);[['Espèces',185000],['Wave',96500],['Orange Money',142000],['Espèces',64000],['Carte',210000]].forEach((p,k)=>{v.push({numero:'T'+i+k,total:p[1]+i*4500+k*1000,paiement:p[0],cree_le:dd+'T10:00:00',annulee:false});});}return v;})(),
 utilisateurs:[{id:'u1',nom:'Direction',role:'admin',actif:true},{id:'u2',nom:'Assistant comptable',role:'assistant',actif:true},{id:'u3',nom:'Stagiaire',role:'assistant',actif:true}],
 messages_internes:[], vx_ia_prompt:[]
};
// les 3 dernières journées caisse déjà intégrées
E.push({id:'ec1',entreprise_id:ENT,journal_code:'VE',date_ecriture:d(4),piece:'CAISSE-'+d(4),libelle:'Recettes Caisse',statut:'valide',numero:'VE-2026-09999'});
['5','6','7','8','9'].forEach(x=>E.push({id:'ec'+x,entreprise_id:ENT,journal_code:'VE',date_ecriture:d(+x),piece:'CAISSE-'+d(+x),libelle:'Recettes Caisse',statut:'valide',numero:'VE-2026-0999'+x}));
function Q(t){this.t=t;this.one=false;this.lim=null;}
['select','eq','order','neq','gte','lte','in','is','not','or','filter','match','ilike','like','range'].forEach(m=>Q.prototype[m]=function(){return this;});
Q.prototype.limit=function(){return this;};
Q.prototype.maybeSingle=function(){this.one=true;return this;};
Q.prototype.single=function(){this.one=true;return this;};
['insert','update','upsert','delete'].forEach(m=>Q.prototype[m]=function(){this.w=true;return this;});
Q.prototype.then=function(res,rej){let data=this.w?null:(DB[this.t]||[]);if(this.one)data=data&&data.length?data[0]:null;return Promise.resolve({data,error:null}).then(res,rej);};
const client={from:t=>new Q(t),rpc:()=>Promise.resolve({data:null,error:null}),storage:{from:()=>({upload:async()=>({}),getPublicUrl:()=>({data:{}})})}};
window.supabase={createClient:()=>client};
window.__DEMO=DB;
})();
