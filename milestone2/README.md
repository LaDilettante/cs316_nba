
We used a csv dataset to obtain the rookie NBA player performance data (1). This is contained in a file called nbarookiedata.csv. This did not contain statistics on draft data, so we found another csv dataset called draft.csv (2). We then used a Python scraper script found on GitHub to obtain NCAA data from Draft Express to a file called ncaa2.csv (3).


(1) https://www.basketball-reference.com/play-index/psl_finder.cgi?request=1&match=single&type=totals&per_minute_base=36&per_poss_base=100&season_start=1&season_end=1&lg_id=NBA&age_min=0&age_max=99&is_playoffs=N&height_min=0&height_max=99&year_min=2001&year_max=2017&birth_country_is=Y&as_comp=gt&as_val=0&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&order_by=season

(2) https://www.basketball-reference.com/play-index/draft_finder.cgi?request=1&year_min=2001&year_max=2016&college_id=0&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&order_by=ws

(3) https://github.com/sshleifer/nbaDraft/blob/master/scrapers/boxscore_stats.py
