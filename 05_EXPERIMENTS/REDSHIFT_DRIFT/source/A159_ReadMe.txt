J/A+A/699/A159      ESPRESSO Redshift Drift Experiment. I.        (Trost+, 2025)
================================================================================
The ESPRESSO Redshift Drift Experiment:
I. High-resolution spectra of the Lyman-alpha forest of QSO J052915.80-435152.0.
    Trost A., Marques C.M.J., Cristiani S., Cupani G., Di Stefano S.,
    D'Odorico V., Guarneri F., Martins C.J.A.P., Milakovic Dinko , Pasquini L.,
    Genova Santos R., Molaro P., Murphy M.T., Nunes N.J., Schmidt T.M.,
    Alibert Y., Boutsia K., Calderone G., Gonzalez Hernandez J.I., Grazian A.,
    Lo Curto G., Palle E., Pepe F., Porru M., Santos N.C., Sozzetti A.,
    Suarez Mascareno A., Zapatero Osorio M.R.
    <Astron. Astrophys. 699, A159 (2025)>
    =2025A&A...699A.159T        (SIMBAD/NED BibCode)
================================================================================
ADC_Keywords: QSOs ; Redshifts ; Spectroscopy
Keywords: instrumentation: spectrographs - quasars: absorption lines -
          cosmology: observations - quasars: individual: J052915.80-435152.0

Abstract:
    The measurement of the temporal evolution in the redshift of distant
    objects, the redshift drift, is a probe of universal expansion and
    cosmology.

    We perform the first steps towards a measurement of such effect using
    the Lyman-alpha forest in the spectra of bright quasars as a tracer of
    cosmological expansion. Our goal is to determine to which precision a
    velocity shift measurement can be carried out with the signal-to-noise
    (S/N) level currently available and whether this precision aligns with
    previous theoretical expectations. A precise assessment of the
    achievable measurement precision is fundamental for estimating the
    time required to carry out the whole project.

    We acquire 12 hours of ESPRESSO observations distributed over 0.875
    years of the brightest quasar known, J052915.80-435152.0 (z=3.962), to
    obtain high-resolution spectra of the Lyman-alpha forest, with median
    S/N of ~86 per 1km/s pixel at the continuum. We divide the
    observations into two epochs and analyse them using both a
    pixel-by-pixel method and a model-based approach. This comparison
    allows us to estimate the velocity shift between the epochs, as well
    as the velocity precision that can be achieved at this S/N. The
    model-based method is calibrated using high-resolution simulations of
    the intergalactic medium, and it provides greater accuracy compared to
    the pixel-by-pixel approach.

    We measure a velocity drift of the Lyman-alpha forest consistent with
    zero: {DELTA}v=-1.25+/-4.45m/s, equivalent to a cosmological drift of
    dv/dt=-1.43+/-5.09m/s/yr or dz/dt=(-2.19+/-7.77)x10^-8^yr^-1^. The
    measurement uncertainties are on par with the expected precision. We
    estimate that reaching a 99% detection of the cosmic drift requires a
    monitoring campaign of 5400 hours of integration time over 54 years
    with an ELT and an ANDES-like high-resolution spectrograph.

Description:
    We set out to assess the feasibility of measuring the redshift drift
    signal using Lyman-alpha forest spectroscopy, based on the
    highest-quality data available prior to the commissioning of
    ELT/ANDES. We used new, high-resolution and high-S/N spectra of the
    most luminous known quasar in the Universe, J052915.80-435152.0 (SB2;
    zem = 3.962), obtained with ESPRESSO at the VLT.

Objects:
    ----------------------------------------------------------------------------
       RA   (2000)   DE       Designation(s)
    ----------------------------------------------------------------------------
    05 29 15.80  -43 51 52.0  QSO J052915.80-435152.0 = SMSS J052915.80-435152.0
    ----------------------------------------------------------------------------

File Summary:
--------------------------------------------------------------------------------
 FileName      Lrecl  Records   Explanations
--------------------------------------------------------------------------------
ReadMe            80        .   This file
tablea1.dat       74      210   Parameters obtained from the fit of all detected
                                 metal transitions with {lambda}>603nm
--------------------------------------------------------------------------------

Byte-by-byte Description of file: tablea1.dat
--------------------------------------------------------------------------------
   Bytes Format Units     Label   Explanations
--------------------------------------------------------------------------------
   1- 29  A29   ---       Trans   Atomic transition
  31- 39  F9.7  ---       z       Redshift of absorption line
  41- 48  E8.3  ---     e_z       Uncertainty on redshift
  50- 55  F6.3  [cm-2]    logN    Logarithmic column density of absorption line
  57- 61  F5.3  [cm-2]  e_logN    Uncertainty on logarithmic column density
  63- 68  F6.3  km/s      b       Doppler parameter of absorption line
  70- 74  F5.3  km/s    e_b       Uncertainty on Doppler parameter
--------------------------------------------------------------------------------

Acknowledgements:
     Andrea Trost, andrea.trost(a)inaf.it

================================================================================
(End)                                        Patricia Vannier [CDS]  02-Jun-2025
