function er=erfrompxi(u)
    pxi=u(1:6,1);
    ger=gfrompxi(pxi);
    per=ger(1:3,4);
    Rer=ger(1:3,1:3);
    eR_Rer=eR(Rer);
    er=[per;eR_Rer];




