import html, os
D = os.path.dirname(os.path.abspath(__file__))
E = html.escape
F = '/home/claude/dossier/node_modules/@fontsource/'
FF = ''.join(f"@font-face{{font-family:'Hanken Grotesk';font-weight:{w};src:url(file://{F}hanken-grotesk/files/hanken-grotesk-latin-{w}-normal.woff2)}}" for w in (400, 500, 600, 700, 800))
FF += ''.join(f"@font-face{{font-family:'Fraunces';font-weight:{w};src:url(file://{F}fraunces/files/fraunces-latin-{w}-normal.woff2)}}" for w in (600, 700))

COMMON = [
    ("Pensé pour l'Afrique", "Francs CFA, Wave, Orange Money, MTN, Moov, normes OHADA."),
    ("Partout", "Sur ordinateur, tablette et téléphone, dans le navigateur."),
    ("À vos règles", "Paramétré selon votre organisation, avec formation de vos équipes."),
]

FICHES = [
 dict(slug='Ecole', pill='ÉCOLE', img='ecole.jpg',
  title="Toute votre école,|sous contrôle.",
  sub="Inscriptions, scolarité, notes, bulletins et parents : un seul logiciel pour gérer tout votre établissement, du primaire au supérieur.",
  who="Écoles privées, collèges, lycées, groupes scolaires, centres de formation, universités et grandes écoles.",
  feats=[
   ("Inscriptions", "Fiche élève complète, import de votre liste existante, pré-inscription en ligne par les parents."),
   ("Scolarité", "Échéanciers créés automatiquement, encaissement espèces et Mobile Money, reçu numéroté pour chaque paiement."),
   ("Impayés", "Les retards remontent seuls : qui doit combien, depuis quand. La relance est prête, en un clic."),
   ("Notes et bulletins", "Moyennes, rangs et mentions calculés ; bulletins à votre en-tête, prêts dès la fin des saisies."),
   ("Vie scolaire", "Appel sur téléphone, emploi du temps généré sans conflit, examens et concours."),
   ("Portail parents", "Notes, absences, frais et annonces sur le téléphone des parents ; messages par e-mail ou WhatsApp."),
   ("Supérieur", "UE, crédits, compensation, rattrapage : chaque établissement règle les siens."),
   ("Fin d'année", "Passage en classe supérieure, redoublants et report des impayés en un clic."),
  ]),
 dict(slug='Immobilier', pill='IMMOBILIER', img='immo.jpg',
  title="La gestion immobilière,|enfin automatisée.",
  sub="Biens, locataires, loyers, contrats, reversements et relances : tout le métier d'une agence dans un seul outil.",
  who="Agences immobilières, administrateurs de biens, syndics de copropriété, promoteurs et propriétaires de patrimoine.",
  feats=[
   ("Loyers et quittances", "Tous les loyers du mois avec leur statut ; la quittance sort quand le loyer est soldé."),
   ("Encaissements", "Mobile Money, virement, chèque, espèces ; paiements partiels, honoraires calculés à chaque paiement."),
   ("Impayés et relances", "Classement par ancienneté, trois niveaux de relance par e-mail, message WhatsApp pré-rempli."),
   ("Propriétaires", "Net à reverser calculé, relevés détaillés à l'en-tête de l'agence."),
   ("Baux et conformité", "Du bail à la restitution du dépôt ; caution et avance contrôlées selon la loi ivoirienne de 2019."),
   ("Documents", "Dix modèles prêts : baux, mandats, compromis, avenant, congé, mise en demeure."),
   ("Syndic et vente", "Copropriété, appels de charges, assemblées générales ; pipeline de vente et commissions."),
   ("Automatisation et IA", "Échéancier glissant, rappels, alertes de fin de bail ; l'IA rédige annonces et relances."),
  ]),
 dict(slug='Comptabilite', pill='COMPTABILITÉ', img='compta.jpg',
  title="Votre comptabilité SYSCOHADA,|en temps réel.",
  sub="Saisie assistée par l'IA, états financiers, TVA et obligations fiscales ivoiriennes : tout se calcule pendant que vous travaillez.",
  who="PME, groupes, cabinets comptables, directions financières, associations et ONG soumises au SYSCOHADA.",
  feats=[
   ("Saisie IA", "Décrivez l'opération ou photographiez la facture : l'IA propose l'écriture SYSCOHADA, vous validez."),
   ("Opérations rapides", "Ventes, règlements, factures fournisseurs, salaires : l'écriture est générée sans numéro de compte."),
   ("Tableau de bord", "Résultat, trésorerie, créances, dettes et une analyse en clair : clients à relancer, TVA à prévoir."),
   ("États financiers", "Compte de résultat en cascade, bilan, flux de trésorerie, liasse imprimable."),
   ("TVA et fiscalité", "Fiche de télédéclaration e-impots préparée ; impôts estimés selon votre régime DGI."),
   ("Balance âgée", "Créances par ancienneté, relance WhatsApp en un clic, dettes fournisseurs payées et lettrées."),
   ("Contrôle", "Journal numéroté sans trou, contre-passation, 9 contrôles de révision avec score de fiabilité."),
   ("Équipe et cabinet", "Rôle de saisie sans accès aux résultats, mode brouillard, import Excel et Sage."),
  ]),
 dict(slug='Caisse_Stock', pill='CAISSE & STOCK', img=None,
  title="Vendez plus vite,|perdez moins.",
  sub="Caisse, stock et achats reliés : chaque vente met à jour le stock, chaque journée se clôture sans écart.",
  who="Boutiques, supérettes, pharmacies, quincailleries, restaurants, maquis, bars, hôtels, distributeurs et grossistes.",
  feats=[
   ("Caisse rapide", "Lecture de code-barres, ticket, plusieurs modes de paiement dont Wave, Orange Money, MTN, Moov et carte."),
   ("Adapté à votre métier", "Champs et écrans propres à chaque type d'établissement : pharmacie avec lots, restaurant, commerce."),
   ("Clôture de caisse", "Clôture intelligente de fin de journée, avec détection des écarts et des anomalies."),
   ("Stock", "Entrées, sorties, seuils d'alerte ; réception de marchandise facilitée par photo."),
   ("Achats", "Factures fournisseurs saisies une fois : la dette fournisseur est suivie jusqu'au paiement."),
   ("Assistant IA", "Posez vos questions sur vos ventes, saisie vocale, analyses du jour."),
   ("Comptabilité reliée", "Chaque journée de ventes devient une écriture comptable en un clic, sans doublon."),
   ("Équipe", "Caissiers, magasiniers, gérant : chacun son accès et ses droits."),
  ]),
 dict(slug='Logistique', pill='LOGISTIQUE', img=None,
  title="Votre flotte et vos livraisons,|sous contrôle.",
  sub="Véhicules, livraisons, carburant, pannes et documents : tout le suivi de votre activité de transport au même endroit.",
  who="Transporteurs, sociétés de livraison, loueurs de véhicules, distributeurs avec flotte, stations-service.",
  feats=[
   ("Flotte", "Fiche de chaque véhicule, affectations, kilométrage et historique."),
   ("Livraisons", "Suivi des tournées et des livraisons, taux de service mesuré."),
   ("Carburant", "Approvisionnement et distribution, suivi des cuves pour les stations-service."),
   ("Pannes et maintenance", "Interventions, coûts et immobilisations suivis par véhicule."),
   ("Documents", "Assurances, visites techniques et pièces du véhicule avec leurs échéances."),
   ("Tableaux de bord", "Graphiques d'activité, pannes, maintenance et documents en temps réel."),
   ("Import Excel", "Reprise de vos fichiers existants ; véhicules manquants créés automatiquement."),
   ("Plateforme VREMAX", "Se relie à la comptabilité, au stock et au budget, avec la même connexion."),
  ]),
]

SURMESURE = dict(slug='Sur_mesure', pill='SUR MESURE', img=None,
  title="Le logiciel de votre organisation,|construit pour elle.",
  sub="Logiciels de gestion, applications web et mobiles, automatisation : Digital-Ivoire conçoit et déploie l'outil qui correspond exactement à votre fonctionnement.",
  who="Groupes et holdings, industries, BTP, transport et logistique, distribution, hôtellerie, santé privée, éducation, institutions et ONG.",
  feats=[
   ("Logiciel de gestion sur mesure", "Ventes, achats, stocks, production, finance, RH : vos processus, vos règles, vos documents."),
   ("Applications mobiles", "Pour vos équipes terrain : collecte, livraisons, inventaires, interventions, même avec peu de réseau."),
   ("Automatisation", "Relances, alertes, rapports et tableaux de bord qui partent seuls, au bon destinataire."),
   ("Paiements", "Mobile Money, encaissements et rapprochements intégrés à vos flux."),
   ("Intelligence artificielle", "Lecture de documents, saisie assistée, analyses et assistants intégrés à l'outil."),
   ("Grandes structures", "Multi-sites, rôles et droits fins, conçu pour accompagner des milliers d'utilisateurs."),
  ],
  steps=["Rencontre et analyse de votre organisation, sur place", "Maquette interactive à valider avant tout développement", "Développement, reprise de vos données et déploiement", "Formation de vos équipes et accompagnement"],
  ref="Référence : un groupe ivoirien de négoce et de production de matériaux, entièrement automatisé avec Digital-Ivoire : ventes, stocks, production, collecte terrain, facturation et tableaux de bord.")


def title_html(t):
    a, _, b = t.partition('|')
    return f"{E(a)}<br><span style='color:#0F6B57'>{E(b)}</span>"


def page(d):
    feats = ''.join(f"<div class='f'><div class='ft'>{E(a)}</div><div class='fd'>{E(b)}</div></div>" for a, b in d['feats'])
    common = ''.join(f"<div class='c'><div class='ct'>{E(a)}</div><div class='cd'>{E(b)}</div></div>" for a, b in COMMON)
    shot = f"<div class='shot'><img src='file://{D}/img/{d['img']}'></div>" if d.get('img') else ''
    steps = ''
    if d.get('steps'):
        steps = "<div class='sec'>Notre méthode</div><div class='steps'>" + ''.join(f"<div class='st'><div class='sn'>{i}</div><div>{E(s)}</div></div>" for i, s in enumerate(d['steps'], 1)) + "</div>"
    ref = f"<div class='ref'>{E(d['ref'])}</div>" if d.get('ref') else ''
    return f"""<!doctype html><html lang='fr'><head><meta charset='utf-8'><style>{FF}
@page{{size:A4;margin:0}}
*{{box-sizing:border-box}}body{{margin:0;font-family:'Hanken Grotesk',sans-serif;color:#14201A}}
.pg{{width:210mm;height:297mm;position:relative;overflow:hidden;background:#F6F3EC;display:flex;flex-direction:column}}
.hd{{background:#14201A;color:#fff;padding:30px 44px 26px}}
.brand{{display:flex;align-items:center;gap:12px}}
.brand img{{width:40px;height:40px;border-radius:9px}}
.bn{{font-family:Fraunces;font-weight:700;font-size:22px;letter-spacing:.2em}}
.pill{{font-family:Fraunces;font-weight:700;font-size:13px;letter-spacing:.14em;background:#3DBE8B;color:#14201A;border-radius:7px;padding:5px 10px 4px}}
h1{{font-family:Fraunces;font-weight:700;font-size:38px;line-height:1.08;margin:24px 0 12px;letter-spacing:-.01em}}
h1 span{{color:#7FD9B3!important}}
.sub{{font-size:15px;line-height:1.5;color:#C9D6CF;max-width:600px}}
.bd{{padding:22px 44px 18px;flex:1;display:flex;flex-direction:column;gap:14px}}
.shot{{border-radius:12px;overflow:hidden;border:6px solid #14201A;height:165px;box-shadow:0 10px 24px -10px rgba(0,0,0,.4)}}
.shot img{{width:100%;height:100%;object-fit:cover;object-position:left top;display:block}}
.sec{{font-size:11px;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:#0F6B57}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px 16px}}
.f{{background:#fff;border-radius:10px;padding:12px 14px;border-left:4px solid #0F6B57}}
.ft{{font-weight:800;font-size:14px;margin-bottom:2px}}
.fd{{font-size:12px;line-height:1.45;color:#3E4B44}}
.who{{font-size:13px;line-height:1.5;background:#E4EFE8;border-radius:10px;padding:9px 12px}}
.who b{{color:#0A5042}}
.cs{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}}
.c{{border-top:3px solid #3DBE8B;padding-top:6px}}
.ct{{font-family:Fraunces;font-weight:700;font-size:15px}}
.cd{{font-size:11.5px;color:#3E4B44;line-height:1.4;margin-top:2px}}
.steps{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}}
.st{{background:#fff;border-radius:10px;padding:12px;font-size:12px;line-height:1.4;font-weight:600}}
.sn{{width:24px;height:24px;border-radius:50%;background:#14201A;color:#3DBE8B;font-family:Fraunces;font-weight:700;display:flex;align-items:center;justify-content:center;margin-bottom:6px}}
.ref{{font-size:13px;line-height:1.5;border:1.5px solid #0F6B57;border-radius:10px;padding:10px 12px;color:#0A5042;font-weight:600}}
.ft2{{margin-top:auto;background:#0F6B57;color:#fff;padding:16px 44px;display:flex;justify-content:space-between;align-items:center}}
.ft2 .l{{font-family:Fraunces;font-weight:700;font-size:17px}}
.ft2 .r{{font-size:12px;font-weight:700;text-align:right;line-height:1.5}}
</style></head><body><div class='pg'>
<div class='hd'><div class='brand'><img src='file://{D}/img/logo.png'><div class='bn'>VREMAX</div><div class='pill'>{E(d['pill'])}</div></div>
<h1>{title_html(d['title'])}</h1><div class='sub'>{E(d['sub'])}</div></div>
<div class='bd'>{shot}
<div class='sec'>Ce que {'nous faisons' if d.get('steps') else 'le logiciel fait pour vous'}</div><div class='grid'>{feats}</div>
{steps}{ref}
<div class='who'><b>Pour qui :</b> {E(d['who'])}</div>
<div class='cs'>{common}</div>
</div>
<div class='ft2'><div class='l'>Rencontrons-nous : notre équipe se déplace.</div><div class='r'>+225 05 74 99 96 75<br>hello@vremaxx.com · www.vremaxx.com</div></div>
</div></body></html>"""


if __name__ == '__main__':
    for d in FICHES + [SURMESURE]:
        open(f"{D}/out/{d['slug']}.html", 'w').write(page(d))
    print('ok')
