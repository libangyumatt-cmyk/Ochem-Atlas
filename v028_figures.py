"""Original, equation-matched teaching mechanisms. No computed geometry is implied.

Electron-pair arrows in the multi-stage sheets run between explicitly named
electron sources and destinations; structural formulas above give the exact
intermediate before and after each row. This avoids implying a single-step
solvent relay in the Fischer teaching pathway.
"""
from html import escape
from build_figures import OUT

INK = '#203c43'
ARROW = '#aa6a4e'


def t(x, y, value, size=23, color=INK, weight='normal'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(value)}</text>'


def line(x1, y1, x2, y2, dashed=False, width=2.7):
    dash = ' stroke-dasharray="6 6"' if dashed else ''
    return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{INK}" stroke-width="{width}" fill="none"{dash}/>'


def curve(d):
    return f'<path d="{d}" fill="none" stroke="{ARROW}" stroke-width="2.8" marker-end="url(#pair)"/>'


def sheet(name, title, body, height, subtitle):
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {height}" role="img" '
            f'aria-label="{escape(title)}"><title>{escape(title)}</title><desc>{escape(subtitle)}</desc>'
            f'<rect width="1200" height="{height}" fill="#fffefa"/>'
            '<defs><marker id="pair" viewBox="0 0 12 12" refX="10" refY="6" '
            'markerWidth="7" markerHeight="7" orient="auto">'
            f'<path d="M1 1L10 6L1 11" fill="none" stroke="{ARROW}" stroke-width="1.7"/>'
            '</marker></defs><g font-family="DejaVu Sans,Arial,sans-serif">')
    (OUT / (name + '.svg')).write_text(head + body + '</g></svg>', encoding='utf-8')


# The anti H-Cβ-Cα-Br dihedral is 180 degrees in the drawn planar conformer.
# Both beta methyl groups are equivalent in this substrate; propene has no E/Z.
b = t(34, 42, 'E2: 2-bromopropane + ethoxide → propene + ethanol + bromide', 25, weight='bold')
b += t(38, 88, 'One concerted event · anti β-H and Br · no carbocation', 20)
b += t(279, 184, 'CβH₂', 26) + t(483, 184, 'CαH', 26) + t(680, 184, 'CH₃', 25)
b += line(363, 173, 474, 173) + line(535, 173, 672, 173)
b += t(289, 112, 'Hβ', 25) + line(328, 123, 328, 150)
b += t(480, 246, 'Br', 25) + line(510, 191, 510, 218)
b += t(35, 293, ':OEt⁻', 25)
b += curve('M118 270 C124 176 198 100 290 105')
b += curve('M327 137 C369 80 422 91 447 159')
b += curve('M511 198 C582 249 582 284 512 282')
b += t(529, 292, 'Br', 23) + t(780, 184, '→  CH₂=CHCH₃', 26)
b += t(782, 226, '+ EtOH + Br⁻', 24)
b += t(35, 343, 'Curved arrows: O lone pair → Hβ; Cβ–H pair → Cβ=Cα; Cα–Br pair → Br.', 19)
b += t(35, 378, 'CβH₂ plus the displayed Hβ is a methyl group; Hβ–Cβ–Cα–Br is anti-periplanar.', 18)
sheet('e2', 'Exact E2 elimination of 2-bromopropane by ethoxide', b, 410,
      'Three concerted electron-pair arrows form propene, ethanol and bromide. Anti alignment is shown.')


# Six-cycle vertices C1-C2-C3-C4-C5-C6. Only C2=C3 remains after closure.
b = t(35, 45, 'Thermal [4+2]: s-cis 1,3-butadiene + ethene → cyclohexene', 26, weight='bold')
b += t(45, 96, 'Diene', 21) + t(200, 385, 'Ethene dienophile', 19) + t(917, 96, 'Product', 21)
p = {'1':(122,220),'2':(205,165),'3':(305,165),'4':(388,220),'5':(305,310),'6':(205,310)}
for a,c in [('1','2'),('2','3'),('3','4'),('5','6')]:
    b += line(*p[a],*p[c]);
for a,c,dx,dy in [('1','2',10,12),('3','4',-10,12),('5','6',0,-9)]:
    x1,y1=p[a];x2,y2=p[c];b+=line(x1+dx,y1+dy,x2+dx,y2+dy,width=2)
b += t(58, 226, 'C1H₂', 17) + t(181, 147, 'C2H', 17) + t(291, 147, 'C3H', 17) + t(396, 226, 'C4H₂', 17)
b += t(175, 343, 'C6H₂', 17) + t(292, 343, 'C5H₂', 17)
b += line(*p['4'],*p['5'],True,1.7) + line(*p['6'],*p['1'],True,1.7)
b += curve('M158 196 C103 184 77 221 158 265')
b += curve('M340 194 C352 251 273 240 257 186')
b += curve('M257 300 C294 266 337 250 353 258')
b += t(488, 270, '→', 45)
# An independent product connectivity drawing. Topological atom labels are
# intentional; they let a reader follow both forming bonds unambiguously.
q={'1':(702,220),'2':(785,165),'3':(885,165),'4':(968,220),'5':(885,310),'6':(785,310)}
for a,c in [('1','2'),('2','3'),('3','4'),('4','5'),('5','6'),('6','1')]:b+=line(*q[a],*q[c])
b += line(785,176,885,176,width=2)
for k,(dx,dy) in {'1':(-35,-8),'2':(-13,-20),'3':(2,-20),'4':(11,-8),'5':(11,25),'6':(-33,25)}.items():
    x,y=q[k];b+=t(x+dx,y+dy,'C'+k,16)
b += t(48, 423, 'Three cyclic pair arrows: C1=C2 → C1–C6; C5=C6 → C4–C5; C3=C4 → C2=C3.', 19)
b += t(48, 459, 'Dashes mark forming bonds, not a stepwise intermediate. This unsubstituted model has no stereocenters.', 17)
b += t(48, 486, 'Both components engage suprafacially; an s-cis diene arrangement brings its termini together.', 17)
sheet('diels-alder', 'Exact butadiene and ethene cycloaddition', b, 520,
      'One six-electron concerted event. Three cyclic electron-pair arrows give cyclohexene.')


b=t(36,44,'Carbonyl addition: R₂C=O + Nu⁻ → R₂C(O⁻)Nu',26,weight='bold')
b+=t(48,105,'R',26)+t(48,292,'R',26)+t(230,184,'C',32)+t(248,73,'O',30)
b+=line(73,114,222,169)+line(72,279,222,190)+line(245,158,259,89)+line(255,159,269,90)
b+=t(30,189,':Nu⁻',28)+curve('M125 178 C142 99 194 112 228 159')
b+=curve('M251 125 C191 67 200 42 244 63')
b+=t(437,184,'→',42)
b+=t(663,91,'O⁻',27)+t(641,193,'C',30)+t(489,155,'R',25)+t(504,290,'R',25)+t(771,178,'Nu',27)
b+=line(656,162,668,107)+line(634,177,519,153)+line(636,207,531,270,True)+line(673,182,760,170,width=5)
b+=t(45,358,'Lone pair on Nu⁻ → carbonyl C; C=O π pair → O. Net charge stays −1.',20)
b+=t(45,394,'The carbonyl is planar; the new tetrahedral alkoxide has an unspecified face of attack.',18)
b+=t(45,424,'Solid wedge / dashed bond indicate depth; identical R groups make this schematic center achiral.',17)
sheet('carbonyl-add', 'Exact generic carbonyl nucleophilic-addition event', b, 455,
      'The local event ends at the alkoxide. Protonation is not part of this reaction equation.')


def sequence(name,title,overall,rows,footer):
    """Each row shows charge-balanced condensed structures and all electron-pair moves.

    Arrow labels in the lower strip denote the electron origins and targets; a
    listed grouped proton relay is expanded to two microscopic transfers.
    """
    rowheight=225
    body=t(32,43,title,26,weight='bold')+t(32,77,overall,21)
    for i,(label,left,right,moves,note) in enumerate(rows):
        y=115+i*rowheight
        chunk=f'<rect x="25" y="{y}" width="1150" height="{rowheight-9}" rx="12" fill="{("#f5f5ee" if i%2==0 else "#faf8f2")}"/>'
        chunk+=t(45,y+31,f'{i+1:02d}  {label}',19,weight='bold')
        chunk+=t(45,y+76,left,19)+t(605,y+76,'→  '+right,19)
        chunk+=t(45,y+107,note,15)
        n=len(moves)
        for j,(origin,target) in enumerate(moves):
            x=51+j*(1090/n)
            width=990/n
            # Stack origin and target labels inside each arrow lane. This
            # keeps the four-arrow solvent relay readable without collisions.
            chunk+=t(x,y+143,origin,13)
            chunk+=curve(f'M{x+15} {y+153} C{x+44} {y+164} {x+90} {y+165} {x+108} {y+180}')
            chunk+=t(x+88,y+202,target,13)
        body+=chunk
        # An event sheet is composed from the identical reviewed row, without
        # redrawing atoms or arrows. The grouped Fischer relay remains labeled.
        event=t(32,43,title+' · stage '+str(i+1),25,weight='bold')
        event+=t(32,77,'Focused stage from the complete pathway; see overview for continuity.',17)
        event+=f'<g transform="translate(0,-{i*rowheight})">{chunk}</g>'
        sheet(f'{name}-step-{i+1}',title+' · '+label,event,360,
              'Exact selected teaching stage extracted from the complete original mechanism sheet.')
    height=115+len(rows)*rowheight+70
    body+=t(39,height-39,footer,17)
    sheet(name,title,body,height,'Complete teaching pathway, with charges and individual electron-pair moves explicitly traced in each row.')


sequence('fischer-esterification','Fischer esterification: acetic acid + ethanol',
         'CH₃CO₂H + HOCH₂CH₃ ⇌ CH₃CO₂CH₂CH₃ + H₂O  (H₃O⁺ catalyst)',[
  ('Carbonyl O protonation','CH₃C(=O)OH + H₃O⁺','CH₃C(=OH⁺)OH + H₂O',
   [('n(carbonyl O)','H of H₃O⁺'),('O–H bond of H₃O⁺','water O')],
   'O of the original carbonyl carries +1; catalyst is temporarily consumed.'),
  ('Ethanol addition','CH₃C(=OH⁺)OH + HOCH₂CH₃','CH₃C(OH)(OH)(O⁺HCH₂CH₃)',
   [('n(ethanol O)','acyl C'),('π(C=O)','original carbonyl O')],
   'Tetrahedral oxonium: the incoming ethanol O now has three bonds and +1.'),
  ('Solvent-mediated proton relay','CH₃C(OH)(OH)(O⁺HCH₂CH₃)','CH₃C(OH)(OH₂⁺)(OCH₂CH₃)',
   [('n(H₂O)','H on ethoxy O⁺'),('O–H on ethoxy O⁺','ethoxy O'),
    ('n(original acid OH)','H of H₃O⁺'),('O–H of H₃O⁺','water O')],
   'Via CH₃C(OH)(OH)(OCH₂CH₃) + H₃O⁺; two transfers, net catalyst-neutral.'),
  ('Tetrahedral collapse','CH₃C(OH)(OH₂⁺)(OCH₂CH₃)','CH₃C(=OH⁺)OCH₂CH₃ + H₂O',
   [('n(original carbonyl OH)','π(C=O)'),('C–OH₂⁺ bond','departing H₂O O')],
   'Water leaves; the original carbonyl O forms the protonated ester carbonyl.'),
  ('Deprotonation','CH₃C(=OH⁺)OCH₂CH₃ + H₂O','CH₃CO₂CH₂CH₃ + H₃O⁺',
   [('n(H₂O)','H on carbonyl O⁺'),('O–H on carbonyl O⁺','ester O')],
   'Hydronium is regenerated; net reaction loses one water molecule.')],
         'No stereogenic product center. The relay is grouped in the card, not a verified single elementary event.')

sequence('imine-formation','Imine formation: acetone + methylamine',
         '(CH₃)₂C=O + CH₃NH₂ ⇌ (CH₃)₂C=NCH₃ + H₂O  (mild H₃O⁺)',[
  ('Carbonyl O protonation','(CH₃)₂C=O + H₃O⁺','(CH₃)₂C=OH⁺ + H₂O',
   [('n(carbonyl O)','H of H₃O⁺'),('O–H bond of H₃O⁺','water O')],
   'The O-protonated ketone is more electrophilic; free amine must remain available.'),
  ('Methylamine addition','(CH₃)₂C=OH⁺ + CH₃NH₂','(CH₃)₂C(OH)(N⁺H₂CH₃)',
   [('n(amine N)','carbonyl C'),('π(C=O)','former carbonyl O')],
   'Carbinolammonium: N has four bonds and +1; O is neutral OH.'),
  ('N deprotonation','(CH₃)₂C(OH)(N⁺H₂CH₃) + H₂O','(CH₃)₂C(OH)(NHCH₃) + H₃O⁺',
   [('n(H₂O)','H of N⁺H₂'),('N–H bond','amine N')],
   'Neutral carbinolamine has one N–H bond.'),
  ('OH activation','(CH₃)₂C(OH)(NHCH₃) + H₃O⁺','(CH₃)₂C(OH₂⁺)(NHCH₃) + H₂O',
   [('n(carbinolamine O)','H of H₃O⁺'),('O–H bond of H₃O⁺','water O')],
   'Protonation creates the H₂O leaving group; the N lone pair remains available.'),
  ('Dehydration / iminium','(CH₃)₂C(OH₂⁺)(NHCH₃)','(CH₃)₂C=N⁺(H)CH₃ + H₂O',
   [('n(N)','π(C=N)'),('C–OH₂⁺ bond','departing H₂O O')],
   'N becomes positively charged on making the second C–N bond.'),
  ('Iminium deprotonation','(CH₃)₂C=N⁺(H)CH₃ + H₂O','(CH₃)₂C=NCH₃ + H₃O⁺',
   [('n(H₂O)','iminium N–H'),('N–H bond','imine N')],
   'Acid is regenerated. Two identical acetone methyl groups give no E/Z isomers.')],
         '1113 for C=N formation is a provisional SORG analogy; no codebook definition is altered.')

print('Built five v0.2.8 original mechanism illustrations.')
