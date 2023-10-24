
time = clock.signals.values(:,1);
datalength = length(time);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%         error          %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

ea1 = e_a.signals.values(:,2);
ea2 = e_a.signals.values(:,3);
ea3 = e_a.signals.values(:,4);
ea4 = e_a.signals.values(:,5);
ea5 = e_a.signals.values(:,6);
ea6 = e_a.signals.values(:,7);

eeo1 = eeo.signals.values(:,2);
eeo2 = eeo.signals.values(:,3);
eeo3 = eeo.signals.values(:,4);
eeo4 = eeo.signals.values(:,5);
eeo5 = eeo.signals.values(:,6);
eeo6 = eeo.signals.values(:,7);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%   input or velocity    %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Vwc1 = Vwc.signals.values(:,2);
Vwc2 = Vwc.signals.values(:,3);
Vwc3 = Vwc.signals.values(:,4);
Vwc4 = Vwc.signals.values(:,5);
Vwc5 = Vwc.signals.values(:,6);
Vwc6 = Vwc.signals.values(:,7);

Vwo1 = Vwo.signals.values(:,2);
Vwo2 = Vwo.signals.values(:,3);
Vwo3 = Vwo.signals.values(:,4);
Vwo4 = Vwo.signals.values(:,5);
Vwo5 = Vwo.signals.values(:,6);
Vwo6 = Vwo.signals.values(:,7);

Vwa1 = Vwa.signals.values(:,2);
Vwa2 = Vwa.signals.values(:,3);
Vwa3 = Vwa.signals.values(:,4);
Vwa4 = Vwa.signals.values(:,5);
Vwa5 = Vwa.signals.values(:,6);
Vwa6 = Vwa.signals.values(:,7);

ueo1 = ueo.signals.values(:,2);
ueo2 = ueo.signals.values(:,3);
ueo3 = ueo.signals.values(:,4);
ueo4 = ueo.signals.values(:,5);
ueo5 = ueo.signals.values(:,6);
ueo6 = ueo.signals.values(:,7);

ua1 = ua.signals.values(:,2);
ua2 = ua.signals.values(:,3);
ua3 = ua.signals.values(:,4);
ua4 = ua.signals.values(:,5);
ua5 = ua.signals.values(:,6);
ua6 = ua.signals.values(:,7);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%     image features     %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

fcox1 = fco.signals.values(:,2);
fcoy1 = fco.signals.values(:,3);
fcox2 = fco.signals.values(:,4);
fcoy2 = fco.signals.values(:,5);
fcox3 = fco.signals.values(:,6);
fcoy3 = fco.signals.values(:,7);
fcox4 = fco.signals.values(:,8);
fcoy4 = fco.signals.values(:,9);

fco_barx1 = fco_bar.signals.values(:,2);
fco_bary1 = fco_bar.signals.values(:,3);
fco_barx2 = fco_bar.signals.values(:,4);
fco_bary2 = fco_bar.signals.values(:,5);
fco_barx3 = fco_bar.signals.values(:,6);
fco_bary3 = fco_bar.signals.values(:,7);
fco_barx4 = fco_bar.signals.values(:,8);
fco_bary4 = fco_bar.signals.values(:,9);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%          pose          %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

pwcx = pwc.signals.values(:,2);
pwcy = pwc.signals.values(:,3);
pwcz = pwc.signals.values(:,4);
zetawcx = zetawc.signals.values(:,2);
zetawcy = zetawc.signals.values(:,3);
zetawcz = zetawc.signals.values(:,4);

pcox_1 = pco1.signals.values(:,2);
pcoy_1 = pco1.signals.values(:,3);
pcoz_1 = pco1.signals.values(:,4);
zetacox_1 = zetaco1.signals.values(:,2);
zetacoy_1 = zetaco1.signals.values(:,3);
zetacoz_1 = zetaco1.signals.values(:,4);

pcox_2 = pco2.signals.values(:,2);
pcoy_2 = pco2.signals.values(:,3);
pcoz_2 = pco2.signals.values(:,4);
zetacox_2 = zetaco2.signals.values(:,2);
zetacoy_2 = zetaco2.signals.values(:,3);
zetacoz_2 = zetaco2.signals.values(:,4);

pwox = pwo.signals.values(:,2);
pwoy = pwo.signals.values(:,3);
pwoz = pwo.signals.values(:,4);
zetawox = zetawo.signals.values(:,2);
zetawoy = zetawo.signals.values(:,3);
zetawoz = zetawo.signals.values(:,4);

pco_barx = pco_bar.signals.values(:,2);
pco_bary = pco_bar.signals.values(:,3);
pco_barz = pco_bar.signals.values(:,4);
zetaco_barx = zetaco_bar.signals.values(:,2);
zetaco_bary = zetaco_bar.signals.values(:,3);
zetaco_barz = zetaco_bar.signals.values(:,4);

padx = pad.signals.values(:,2);
pady = pad.signals.values(:,3);
padz = pad.signals.values(:,4);
zetaadx = zetaad.signals.values(:,2);
zetaady = zetaad.signals.values(:,3);
zetaadz = zetaad.signals.values(:,4);

paox = pao.signals.values(:,2);
paoy = pao.signals.values(:,3);
paoz = pao.signals.values(:,4);
zetaaox = zetaao.signals.values(:,2);
zetaaoy = zetaao.signals.values(:,3);
zetaaoz = zetaao.signals.values(:,4);