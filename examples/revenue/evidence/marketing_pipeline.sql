-- Marketing pipeline report
select
  date_trunc('month', created_date) as month,
  sum(pipeline_amount) as pipeline_revenue,
  sum(weighted_pipeline_amount) as weighted_pipeline
from mart.marketing_sourced_pipeline
where opportunity_stage in ('Open', 'Qualified', 'Proposal')
group by 1;
