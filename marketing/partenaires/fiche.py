# Fiche "Programme partenaires" (style VREMAX), réutilise le gabarit des fiches modules.
import sys, os
sys.path.insert(0, sys.argv[1])  # dossier contenant gen.py (+ img/)
import gen
d = dict(slug='Partenaires', pill='PARTENAIRES', img=None,
  title="Recommandez-nous,|touchez 10 %.",
  sub="Vous connaissez des entreprises qui ont besoin de mieux s'organiser ? Présentez-les à Digital-Ivoire : notre équipe s'occupe de tout, vous êtes rémunéré à chaque contrat signé.",
  who="Experts-comptables et cabinets, consultants, informaticiens indépendants, vendeurs de matériel informatique et de caisse, commerciaux terrain, formateurs, et toute personne bien introduite auprès des entreprises.",
  feats=[
   ("10 % de commission", "Sur le montant de mise en place payé par le client que vous nous présentez, versée à chaque encaissement."),
   ("Exemples", "Module VREMAX à 2 200 000 F : 220 000 F pour vous. Projet sur mesure à 15 000 000 F : 1 500 000 F."),
   ("Rien à avancer", "Aucun frais, aucun stock, aucun objectif imposé. Vous présentez, nous faisons le reste."),
   ("Nous menons la vente", "Rencontre, démonstration, proforma sous 24 h, déploiement et formation : notre équipe s'en charge."),
   ("Tout se recommande", "Modules VREMAX (école, immobilier, comptabilité, caisse et stock, logistique) et logiciels sur mesure."),
   ("Clients protégés", "Chaque client signalé est enregistré à votre nom pendant 12 mois, confirmé par écrit."),
  ],
  steps=["Vous nous signalez l'entreprise par email ou WhatsApp", "Nous l'enregistrons à votre nom et vous le confirmons", "Notre équipe la rencontre et remet une proforma sous 24 h", "Le client paie : votre commission est versée sous 7 jours"],
  ref="Digital-Ivoire conçoit et déploie des logiciels de gestion pour les entreprises ivoiriennes, dont un groupe de négoce et de production de matériaux entièrement automatisé : ventes, stocks, production, collecte terrain, facturation.")
h = gen.page(d)
h = h.replace("Ce que nous faisons", "Le programme").replace("Notre méthode", "Comment ça marche")
h = h.replace("Rencontrons-nous : notre équipe se déplace.", "Devenez partenaire : écrivez-nous.")
out = os.path.join(sys.argv[1], 'out_p'); os.makedirs(out, exist_ok=True)
open(os.path.join(out, 'Programme_Partenaires.html'), 'w').write(h)
print('ok')
