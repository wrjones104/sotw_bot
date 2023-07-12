import random


def chaos():
    # -----GAME-----
    # SETTINGS
    mode = random.choices(["-open", "-cg"], weights=([1, 7]), k=1)[0]
    slog = random.choices(['', ' -sl'], weights=([13, 1]), k=1)[0]
    settings = ''.join([mode, slog])

    # KEFKA'S TOWER & STATUE SKIP
    ktcr1 = random.randint(3, 9)
    ktcr2 = random.randint(ktcr1, 12)
    kter1 = random.randint(5, 14)
    kter2 = random.randint(kter1, 16)
    ktdr1 = random.randint(1, 6)
    ktdr2 = random.randint(ktdr1, 6)
    stcr1 = random.randint(4, 10)
    stcr2 = random.randint(stcr1, 13)
    ster1 = random.randint(6, 15)
    ster2 = random.randint(ster1, 17)
    stdr1 = random.randint(2, 7)
    stdr2 = random.randint(stdr1, 7)
    stno = random.choices([True, False], weights=([4, 1]), k=1)[0]

    if stno:
        kt = '.'.join([' -oa 2.2.2.2', str(ktcr1), str(ktcr2), '4', str(kter1), str(kter2), '6', str(ktdr1),
                       str(ktdr2)])
    else:
        kt = '.'.join([' -oa 2.2.2.2', str(ktcr1), str(ktcr2), '4', str(kter1), str(kter2), '6', str(ktdr1),
                       str(ktdr2)])
        kt += '.'.join([' -ob 3.2.2.2', str(stcr1), str(stcr2), '4', str(ster1), str(ster2), '6', str(stdr1),
                        str(stdr2)])

    objectives = random.choice([' -oc 0.1.1.1.r', ' -oc 0.1.1.1.r -od 0.1.1.1.r',
                                ' -oc 0.1.1.1.r -od 0.1.1.1.r -oe 0.1.1.1.r',
                                ' -oc 0.1.1.1.r -od 0.1.1.1.r -oe 0.1.1.1.r -of 0.1.1.1.r'])
    objectives += ' -og 59.1.1.1.r'
    game = ''.join([settings, kt, objectives])

    # -----PARTY-----
    # STARTING PARTY
    sc1 = random.choice([' -sc1 random', ' -sc1 randomngu'])
    sc2 = random.choice([' -sc2 random', ' -sc2 randomngu'])
    sc3 = random.choices([' -sc3 random', ' -sc3 randomngu', ''], weights=([1, 1, 5]), k=1)[0]
    sc4 = random.choices([' -sc4 random', ' -sc4 randomngu', ''], weights=([1, 1, 10]), k=1)[0]
    slevel = random.choices(['', ''.join([' -stl ', str(random.randint(3, 9))])], weights=([10, 1]), k=1)[0]
    sparty = ''.join([sc1, sc2, sc3, sc4, slevel])

    # SWORDTECHS
    fst = random.choices([' -fst', ''], weights=([1, 0]), k=1)[0]
    sel = random.choices([' -sel', ''], weights=([1, 3]), k=1)[0]
    swdtech = ''.join([fst, sel])

    # BLITZES
    brl = random.choices([' -brl', ''], weights=([5, 1]), k=1)[0]
    bel = random.choices([' -bel', ''], weights=([1, 5]), k=1)[0]
    blitz = ''.join([brl, bel])

    # LORES
    slr1 = random.randint(0, 12)
    slr2 = random.randint(slr1, 16)
    slrr = ' '.join([' -slr', str(slr1), str(slr2)])
    slr = random.choices([slrr, ''], weights=([5, 1]), k=1)[0]
    lmprp1 = random.randint(25, 125)
    lmprp2 = random.randint(lmprp1, 175)
    lmprv1 = random.randint(10, 60)
    lmprv2 = random.randint(lmprv1, 80)
    lmprp = ' '.join([' -lmprp', str(lmprp1), str(lmprp2)])
    lmprv = ' '.join([' -lmprv', str(lmprv1), str(lmprv2)])
    loremp = random.choices(['', ' -lmps', lmprp, lmprv], weights=([1, 3, 5, 3]), k=1)[0]
    lel = random.choices([' -lel', ''], weights=([13, 1]), k=1)[0]
    lores = ''.join([slr, loremp, lel])

    # RAGES
    srr1 = random.randint(0, 25)
    srr2 = random.randint(srr1, 50)
    srr = ' '.join([' -srr', str(srr1), str(srr2)])
    srages = random.choices(['', srr], weights=([1, 10]), k=1)[0]
    rnl = random.choices([' -rnl', ''], weights=([1, 0]), k=1)[0]
    rnc = random.choices([' -rnc', ''], weights=([10, 1]), k=1)[0]
    rage = ''.join([srages, rnl, rnc])

    # DANCES
    sdr1 = random.randint(0, 4)
    sdr2 = random.randint(sdr1, 6)
    sdr = ' '.join([' -sdr', str(sdr1), str(sdr2)])
    das = random.choices([' -das', ''], weights=([1, 0]), k=1)[0]
    dda = random.choices([' -dda', ''], weights=([1, 0]), k=1)[0]
    dns = random.choices([' -dns', ''], weights=([1, 0]), k=1)[0]
    d_el = random.choices([' -del', ''], weights=([1, 13]), k=1)[0]
    dance = ''.join([sdr, das, dda, dns, d_el])

    # SKETCH & CONTROL
    scis = random.choice([' -scis', ''])

    # STEAL CHANCES
    steal = random.choice(['', ' -sch', ' -sch', ' -sca', ' -sca', ' -sca'])

    # CHARACTERS
    sal = random.choices([' -sal', ''], weights=([7, 1]), k=1)[0]
    sn = random.choices([' -sn', ''], weights=([1, 7]), k=1)[0]
    eu = random.choices([' -eu', ''], weights=([7, 1]), k=1)[0]
    csrp1 = random.randint(50, 120)
    csrp2 = random.randint(csrp1, 160)
    csrp = ' '.join([' -csrp', str(csrp1), str(csrp2)])
    cstats = ''.join([sal, sn, eu, csrp])

    # COMMANDS
    scc = random.choices([' -scc', ''], weights=([1, 5]), k=1)[0]
    com = random.choices([' -com 99999999999999999999999999', '', ' -com 98989898989898989898989898'],
                         weights=([7, 1, 7]), k=1)[0]
    recskills = ['10', '6', '14', '19', '24', '26', '22', '12', '3', '28', '16', '11', '27', '13', '15', '5',
                 '7', '8', '9', '23', '29']
    rec1 = random.choices([' -rec1 28', ''], weights=([10, 1]), k=1)[0]
    rec2 = random.choices([' -rec2 23', ''], weights=([7, 1]), k=1)[0]
    rec3 = random.choices([' '.join([' -rec3', random.choice(recskills)]), ''], weights=([1, 10]), k=1)[0]
    rec4 = random.choices([' '.join([' -rec4', random.choice(recskills)]), ''], weights=([1, 10]), k=1)[0]
    rec5 = random.choices([' '.join([' -rec5', random.choice(recskills)]), ''], weights=([1, 10]), k=1)[0]
    commands = ''.join([scc, com, rec1, rec2, rec3, rec4, rec5])

    party = ''.join([sparty, swdtech, blitz, lores, rage, dance, cstats, commands, steal, scis])

    # -----BATTLE-----
    xpm = ' '.join([' -xpm', str(random.choices([2, 3, 4, 5, 6], weights=([2, 10, 6, 3, 1]), k=1)[0])])
    gpm = ' '.join([' -gpm', str(random.choices([3, 4, 5, 6, 7, 8, 9, 10], weights=([1, 2, 10, 6, 3, 2, 1, 1]),
                                                k=1)[0])])
    mpm = ' '.join([' -mpm', str(random.choices([3, 4, 5, 6, 7, 8, 9, 10], weights=([1, 2, 10, 6, 3, 2, 1, 1]),
                                                k=1)[0])])
    nxppd = random.choices([' -nxppd', ''], weights=([7, 1]), k=1)[0]
    xpmpgp = ''.join([xpm, gpm, mpm, nxppd])

    # BOSSES
    bb = random.choices([' -bbr', ' -bbs', ''], weights=([5, 10, 1]), k=1)[0]
    bmbd = ' '.join([' -drloc', random.choices(['original', 'shuffle', 'mix'], weights=([1, 5, 1]), k=1)[0]])
    bmbd += ' '.join([' -stloc', random.choices(['original', 'shuffle', 'mix'], weights=([1, 2, 5]), k=1)[0]])
    srp3 = random.choices([' -srp3', ''], weights=([1, 10]), k=1)[0]
    bnds = random.choices([' -bnds', ''], weights=([1, 8]), k=1)[0]
    be = random.choices([' -be', ''], weights=([13, 1]), k=1)[0]
    bnu = random.choices([' -bnu', ''], weights=([10, 1]), k=1)[0]
    bosses = ''.join([bb, bmbd, srp3, bnds, be, bnu])

    # BOSS AI
    dgne = random.choices([' -dgne', ''], weights=([10, 1]), k=1)[0]
    wnz = random.choices([' -wnz', ''], weights=([10, 1]), k=1)[0]
    mmnu = random.choices([' -mmnu', ''], weights=([13, 1]), k=1)[0]
    cmd = random.choices([' -cmd', ''], weights=([1, 0]), k=1)[0]
    b_ai = ''.join([dgne, wnz, mmnu, cmd])

    # SCALING
    scale_opt = ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5']
    lspf = ' '.join([' -lsced', random.choices(scale_opt, weights=([0, 1, 1, 10, 5, 3, 1, 0, 0, 0]), k=1)[0]])
    lsaf = ' '.join([' -lsa', random.choices(scale_opt, weights=([0, 10, 3, 2, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    lshf = ' '.join([' -lsh', random.choices(scale_opt, weights=([0, 10, 3, 2, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    lstf = ' '.join([' -lst', random.choices(scale_opt, weights=([0, 1, 5, 10, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    hmpf = ' '.join([' -hmced', random.choices(scale_opt, weights=([0, 1, 1, 10, 5, 3, 1, 0, 0, 0]), k=1)[0]])
    hmaf = ' '.join([' -hma', random.choices(scale_opt, weights=([0, 10, 3, 2, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    hmhf = ' '.join([' -hmh', random.choices(scale_opt, weights=([0, 10, 3, 2, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    hmtf = ' '.join([' -hmt', random.choices(scale_opt, weights=([0, 1, 5, 10, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    xgpf = ' '.join([' -xgced', random.choices(scale_opt, weights=([0, 1, 1, 10, 5, 3, 1, 0, 0, 0]), k=1)[0]])
    xgaf = ' '.join([' -xga', random.choices(scale_opt, weights=([0, 10, 3, 2, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    xghf = ' '.join([' -xgh', random.choices(scale_opt, weights=([0, 10, 3, 2, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    xgtf = ' '.join([' -xgt', random.choices(scale_opt, weights=([0, 1, 5, 10, 1, 0, 0, 0, 0, 0]), k=1)[0]])
    asrf = ' '.join([' -asr', random.choices(scale_opt, weights=([0, 0, 3, 10, 2, 1, 0, 0, 0, 0]), k=1)[0]])
    asef = ' '.join([' -ase', random.choices(scale_opt, weights=([0, 0, 3, 10, 2, 1, 0, 0, 0, 0]), k=1)[0]])
    lscale = random.choices([lspf, lsaf, lshf, lstf, ''], weights=([7, 2, 2, 1, 0]), k=1)[0]
    hmscale = random.choices([hmpf, hmaf, hmhf, hmtf, ''], weights=([7, 2, 2, 1, 0]), k=1)[0]
    xgscale = random.choices([xgpf, xgaf, xghf, xgtf, ''], weights=([7, 2, 2, 1, 0]), k=1)[0]
    ascale = random.choices([asrf, asef, ''], weights=([1, 7, 0]), k=1)[0]
    msl = ' '.join([' -msl', str(random.randint(45, 80))])
    sfb = random.choices([' -sfb', ''], weights=([0, 1]), k=1)[0]
    sed = random.choices([' -sed', ''], weights=([7, 1]), k=1)[0]
    scaling = ''.join([lscale, hmscale, xgscale, ascale, msl, sfb, sed])

    # ENCOUNTERS
    renc = random.choices(['', ' -res', ' '.join([' -rer', str(random.randint(0, 33))])], weights=([1, 10, 10]), k=1)[0]
    fenc = random.choices(['', ' '.join([' -fer', str(random.randint(0, 33))])], weights=([1, 10]), k=1)[0]
    escr = ' '.join([' -escr', str(random.randint(75, 100))])
    encounters = ''.join([renc, fenc, escr])

    battle = ''.join([bosses, b_ai, scaling, encounters, xpmpgp])

    # -----MAGIC-----
    # ESPERS
    esr1 = random.randint(1, 3)
    esr2 = random.randint(esr1, 5)
    esr = ' '.join([' -esr', str(esr1), str(esr2)])
    ess = random.choices(['', esr, ' -esrr', ' -ess', ' -essrr', ' -esrt'], weights=([1, 7, 2, 2, 2, 3]), k=1)[0]
    ebonus = random.choices(['', ' '.join([' -ebr', str(random.randint(67, 100))]), ' -ebs'], weights=([1, 7, 3]),
                            k=1)[0]
    emprp1 = random.randint(50, 125)
    emprp2 = random.randint(emprp1, 150)
    emprv1 = random.randint(50, 99)
    emprv2 = random.randint(emprv1, 120)
    eer1 = random.randint(3, 8)
    eer2 = random.randint(eer1, 10)
    emprp = ' '.join([' -emprp', str(emprp1), str(emprp2)])
    emprv = ' '.join([' -emprv', str(emprv1), str(emprv2)])
    emp = random.choices(['', emprp, emprv, ' -emps'], weights=([1, 7, 3, 3]), k=1)[0]
    eer = ' '.join([' -eer', str(eer1), str(eer2)])
    eebr = ' '.join([' -eebr', str(random.randint(3, 9))])
    eeq = random.choices([eer, eebr, ''], weights=([1, 2, 7]), k=1)[0]
    ems = random.choices(['', ' -ems'], weights=([7, 1]), k=1)[0]
    espers = ''.join([ess, ebonus, emp, eeq, ems])
    stespr1 = random.randint(1, 2)
    stespr2 = random.randint(stespr1, 4)
    stesp = random.choice(["", ' '.join([' -stesp', str(stespr1), str(stespr2)])])
    espers += stesp

    # NATURAL MAGIC
    nm1 = random.choices(['', ' -nm1 random'], weights=([1, 10]), k=1)[0]
    nm2 = random.choices(['', ' -nm2 random'], weights=([1, 10]), k=1)[0]
    rnl1 = random.choices(['', ' -rnl1'], weights=([0, 1]), k=1)[0]
    rnl2 = random.choices(['', ' -rnl2'], weights=([0, 1]), k=1)[0]
    rns1 = random.choices(['', ' -rns1'], weights=([0, 1]), k=1)[0]
    rns2 = random.choices(['', ' -rns2'], weights=([0, 1]), k=1)[0]
    m_indicator = random.choices(['', ' -nmmi'], weights=([0, 1]), k=1)[0]
    nmagic = ''.join([nm1, nm2, rnl1, rnl2, rns1, rns2, m_indicator])
    mmprp1 = random.randint(50, 125)
    mmprp2 = random.randint(emprp1, 150)
    mmprv1 = random.randint(1, 50)
    mmprv2 = random.randint(emprv1, 99)
    mmp = random.choice(['', ' -mmps', ' '.join([' -mmprv', str(mmprv1), str(mmprv2)]),
                         ' '.join([' -mmprp', str(mmprp1), str(mmprp2)])])
    mmp += random.choices(['', ' -u254'], weights=([10, 1]), k=1)[0]
    nmagic += mmp

    magic = ''.join([espers, nmagic])

    # -----ITEMS-----
    # STARTING GOLD/ITEMS
    gp = ' '.join([' -gp', str(random.randint(0, 100000))])
    smc = ' '.join([' -smc', random.choices(['1', '2', '3'], weights=([1, 2, 7]), k=1)[0]])
    sws = ' '.join([' -sws', str(random.randint(0, 10))])
    sfd = ' '.join([' -sfd', str(random.randint(0, 10))])
    sto = ' '.join([' -sto', str(random.randint(0, 6))])
    s_inv = ''.join([gp, smc, sfd, sto, sws])

    # ITEMS
    ier1 = random.randint(4, 8)
    ier2 = random.randint(ier1, 10)
    ier = ' '.join([' -ier', str(ier1), str(ier2)])
    iebr = ' '.join([' -iebr', str(random.randint(4, 10))])
    ieor = ' '.join([' -ieor', str(random.randint(15, 75))])
    iesr = ' '.join([' -iesr', str(random.randint(15, 75))])
    iequip = random.choices(['', ier, iebr, ieor, iesr], weights=([1, 2, 2, 7, 2]), k=1)[0]
    ierr1 = random.randint(4, 8)
    ierr2 = random.randint(ierr1, 10)
    ierr = ' '.join([' -ierr', str(ierr1), str(ierr2)])
    ierbr = ' '.join([' -ierbr', str(random.randint(4, 10))])
    ieror = ' '.join([' -ieror', str(random.randint(15, 75))])
    iersr = ' '.join([' -iersr', str(random.randint(15, 75))])
    requip = random.choices(['', ierr, ierbr, ieror, iersr], weights=([1, 2, 2, 7, 2]), k=1)[0]
    csb1 = random.randint(1, 32)
    csb2 = random.randint(csb1, 32)
    csb = ' '.join([' -csb', str(csb1), str(csb2)])
    mca = random.choices([' -mca', ''], weights=([13, 1]), k=1)[0]
    stra = random.choices([' -stra', ''], weights=([1, 0]), k=1)[0]
    saw = random.choices([' -saw', ''], weights=([1, 0]), k=1)[0]
    equips = ''.join([iequip, requip, csb, mca, stra, saw])

    # SHOPS
    sisr = ' '.join([' -sisr', str(random.randint(10, 80))])
    shopinv = random.choices(['', sisr, ' -sirt', ' -sie'], weights=([3, 10, 5, 1]), k=1)[0]
    sprv1 = random.randint(0, 65535)
    sprv2 = random.randint(sprv1, 65535)
    sprp1 = random.randint(25, 125)
    sprp2 = random.randint(sprp1, 175)
    sprv = ' '.join([' -sprv', str(sprv1), str(sprv2)])
    sprp = ' '.join([' -sprp', str(sprp1), str(sprp2)])
    shopprices = random.choices(['', sprv, sprp], weights=([1, 2, 7]), k=1)[0]
    ssf = random.choices(['', ' -ssf4', ' -ssf8', ' -ssf0'], weights=([7, 1, 1, 0]), k=1)[0]
    sdm = ' '.join([' -sdm', str(random.randint(3, 5))])
    npi = random.choices(['', ' -npi'], weights=([1, 13]), k=1)[0]
    snbr = random.choices(['', ' -snbr'], weights=([7, 1]), k=1)[0]
    snes = random.choices(['', ' -snes'], weights=([7, 1]), k=1)[0]
    snsb = random.choices(['', ' -snsb'], weights=([7, 1]), k=1)[0]
    shops = ''.join([shopinv, shopprices, ssf, sdm, npi, snbr, snes, snsb])

    # CHESTS
    ccontents = random.choices(['', ' -ccrt', ' -cce', ' '.join([' -ccsr', str(random.randint(10, 80))])],
                               weights=([1, 6, 1, 13]), k=1)[0]
    cms = random.choices(['', ' -cms'], weights=([1, 13]), k=1)[0]
    chests = ''.join([ccontents, cms])

    items = ''.join([s_inv, equips, shops, chests])

    # -----CUSTOM-----
    # SEE CUSTOM_SPRITES_PORTRAITS.PY
    wmhc = random.choice(['', ' -wmhc'])

    # -----OTHER-----
    # COLISEUM
    co = random.choices(['', ' -cor', ' -cos'], weights=([1, 7, 1]), k=1)[0]
    cr = random.choices(['', ' -crs', ' -crr'], weights=([1, 1, 7]), k=1)[0]
    crvr1 = random.randint(20, 80)
    crvr2 = random.randint(crvr1, 150)
    visible = random.choices(['', ' '.join([' -crvr', str(crvr1), str(crvr2)])], weights=([1, 10]), k=1)[0]
    rmenu = random.choices(['', ' -crm'], weights=([1, 13]), k=1)[0]
    colo = ''.join([co, cr, visible, rmenu])

    # AUCTION HOUSE
    ari = random.choices(['', ' -ari'], weights=([0, 1]), k=1)[0]
    anca = random.choices(['', ' -anca'], weights=([0, 1]), k=1)[0]
    adeh = random.choices(['', ' -adeh'], weights=([1, 13]), k=1)[0]
    ah = ''.join([ari, anca, adeh])

    # MISC
    asprint = ' '.join([' -move', random.choice(['as', 'bd', 'ssbd'])])
    ond = random.choices(['', ' -ond'], weights=([1, 13]), k=1)[0]
    rr = random.choices(['', ' -rr'], weights=([1, 13]), k=1)[0]
    scan = random.choices(['', ' -scan'], weights=([13, 1]), k=1)[0]
    etimers = random.choices(['', ' -etr', ' -etn'], weights=([2, 3, 1]), k=1)[0]
    ychoices = [' -ymascot', ' -ycreature', ' -yimperial', ' -ymain', ' -yreflect', ' -ystone', ' -ysketch',
                ' -yrandom', ' -yremove', '']
    ychoice = random.choices(ychoices, weights=([1, 1, 1, 1, 1, 1, 1, 1, 2, 10]), k=1)[0]
    flashes = random.choice(['', ' -frm', ' -frw'])
    warp = random.choice(['', ' -warp'])
    misc = ''.join([asprint, ond, rr, scan, etimers, ychoice, flashes, warp])

    # CHALLENGES
    nmc = random.choices(['', ' -nmc'], weights=([1, 5]), k=1)[0]
    nee = random.choices(['', ' -nee'], weights=([7, 1]), k=1)[0]
    nil = random.choices(['', ' -nil'], weights=([1, 7]), k=1)[0]
    nfps = random.choices(['', ' -nfps'], weights=([1, 13]), k=1)[0]
    if '-u254' in magic:
        nu = ''
    else:
        nu = random.choices(['', ' -nu'], weights=([1, 13]), k=1)[0]
    rls = \
    random.choices(['', ' -rls all', ' -rls grey', ' -rls black', ' -rls white'], weights=([13, 1, 1, 1, 1]), k=1)[0]
    # for x in spells.id_spell.values():
    #     y = random.choices(['', x + ','], weights=([10, 1]), k=1)[0]
    #     nu += y
    # nu = random.choices([nu, nu + "Ultima,"], weights=([1, 10]), k=1)[0]
    # nu = random.choices([' -rls Ultima', "", ' -rls "' + nu[:-1] + '"'], weights=([5, 1, 5]), k=1)[0]
    nfp = random.choices(['', ' -nfce'], weights=([7, 1]), k=1)[0]
    pd = random.choices(['', ' -pd'], weights=([13, 1]), k=1)[0]
    challenges = ''.join([nmc, nee, nil, nfps, nu, nfp, pd, rls])

    # BUG FIXES
    fs = random.choices(['', ' -fs'], weights=([0, 1]), k=1)[0]
    fe = random.choices(['', ' -fe'], weights=([1, 13]), k=1)[0]
    fvd = random.choices(['', ' -fvd'], weights=([1, 13]), k=1)[0]
    fr = random.choices(['', ' -fr'], weights=([1, 13]), k=1)[0]
    fj = random.choices(['', ' -fj'], weights=([0, 1]), k=1)[0]
    fbs = random.choices(['', ' -fbs'], weights=([1, 13]), k=1)[0]
    fedc = random.choices(['', ' -fedc'], weights=([0, 1]), k=1)[0]
    fc = random.choices(['', ' -fc'], weights=([1, 13]), k=1)[0]
    bugfixes = ''.join([fs, fe, fvd, fr, fj, fbs, fedc, fc])

    other = ''.join([colo, ah, challenges, misc, bugfixes])

    flagset = ''.join([game, party, battle, magic, items, other, wmhc])
    return flagset
