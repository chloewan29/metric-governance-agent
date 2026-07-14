-- Sales dashboard query owned by Sales Ops
select
  date_trunc('month', close_date) as month,
  sum(amount) as revenue,
  count(distinct opportunity_id) as closed_won_deals
from crm.opportunities
where stage = 'Closed Won'
  and is_cancelled = false
group by 1;
