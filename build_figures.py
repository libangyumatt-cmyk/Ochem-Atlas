"""Small original, code-native SVG mechanisms. No quantum calculations."""
from pathlib import Path
from html import escape
OUT=Path(__file__).parent/'dist'/'mechanisms'
OUT.mkdir(exist_ok=True)
def text(x,y,s,size=24):return f'<text x="{x}" y="{y}" font-size="{size}">{escape(s)}</text>'
def path(d,arrow=False,fish=False):return f'<path d="{d}" fill="none" stroke="{("#aa6a4e" if arrow else "#203c43")}" stroke-width="2.3"'+(f' marker-end="url(#{"fish" if fish else "pair"})"' if arrow else '')+'/>'
def svg(name,body,height=310):
 head=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 {height}" role="img" aria-label="{name}"><rect width="100%" height="100%" fill="#fffefa"/><defs><marker id="pair" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M1 1L9 5L1 9" fill="none" stroke="#aa6a4e" stroke-width="1.5"/></marker><marker id="fish" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M1 1L9 5" fill="none" stroke="#aa6a4e" stroke-width="1.5"/></marker></defs><g font-family="DejaVu Sans,sans-serif" fill="#203c43">'
 (OUT/(name+'.svg')).write_text(head+body+'</g></svg>')
svg('proton-transfer',text(28,34,'Acetic acid + cyanide: direct proton-transfer model',21)+text(62,130,'⁻:C≡N')+text(285,130,'H')+text(405,130,'O')+text(486,130,'C(=O)CH₃')+path('M310 121H399')+path('M430 121H481')+path('M84 108 C115 47 232 49 285 106',True)+path('M353 119 C369 67 410 72 418 104',True)+text(200,205,'⇌  HCN + CH₃CO₂⁻',26)+text(28,272,'Two electron pairs move. Charge: −1 on each side. Solvent relays are omitted.',17))
svg('lewis',text(28,34,'Ammonia + boron trifluoride: Lewis association',21)+text(125,124,'H₃N:')+text(415,124,'BF₃')+path('M194 105 C249 39 365 45 421 102',True)+text(237,205,'⇌  H₃N⁺–BF₃⁻',28)+text(28,272,'N donates its lone pair to B. The adduct is neutral overall.',18))
svg('radical-combine',text(28,34,'Methyl-radical recombination',21)+text(164,137,'CH₃•')+text(478,137,'•CH₃')+path('M223 117 C246 56 315 53 352 119',True,True)+path('M485 117 C462 56 397 53 363 119',True,True)+text(222,207,'→  CH₃–CH₃',28)+text(28,268,'Each fishhook carries one electron to the new C–C bond.',18)+text(28,293,'A spin-compatible radical pair forms closed-shell ethane.',16),325)
# Condensed structural drawings retain both ring C–O bonds and label all charges.
def ring(x,y,protonated=False):
 b=text(x,y,'CH₃–CH')+text(x+185,y,'CH₂')+text(x+126,y-96,'O⁺H' if protonated else ':O:',23)
 return b+path(f'M{x+110} {y-9}H{x+178}')+path(f'M{x+92} {y-29}L{x+132} {y-78}')+path(f'M{x+188} {y-29}L{x+160} {y-78}')
body=text(28,32,'Propylene oxide + HCl: major HCl/ether pathway',21)+text(28,73,'1  Protonation',18)+ring(85,233)+text(423,138,'H')+text(534,138,'Cl')+path('M448 130H528')+path('M233 110 C288 59 377 67 426 114',True)+path('M486 126 C503 77 551 81 548 111',True)+text(636,174,'Protonated epoxide',18)+text(659,204,'+ Cl⁻',23)+path('M577 170H621',True)
body+=text(28,296,'2  Backside opening at the primary carbon',18)+ring(90,468,True)+text(449,456,':Cl⁻')+path('M451 435 C404 367 338 380 313 438',True)+path('M270 418 C315 366 284 339 251 361',True)+text(520,501,'→  ClCH₂CH(OH)CH₃',25)+text(28,548,'C–O cleavage neutralizes oxygen directly; no third deprotonation step.',18)+text(28,579,'The primary carbon is achiral. The secondary carbon retains its C–O bond.',16)
svg('acid-epoxide',body,610)
print('Built four original mechanism illustrations.')
