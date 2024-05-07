from django.contrib import admin

from django.urls import include
from django.urls import path
from django.shortcuts import redirect

from dashboard_app import views as dashboard_views
from data_app import views as data_views
from manageuser_app import views as manageuser_views
from legal_app import views as legal_views
from report_app import views as report_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    # User Management
    path('', lambda request: redirect('login/'), name='root'),
    path('register/', manageuser_views.register_view, name='register'),
    path('logout/', manageuser_views.logout_view, name='logout'),
    path('login/', manageuser_views.login_view, name='login'),
    path('dashboard/', dashboard_views.board_view, name='dashboard'),

    # Reporting Support-AJAX
    path('view_editable_data_records/', data_views.view_editable_data_records, name='view_editable_data_records'),
    path('edit_data_record/<int:cr_id>/', data_views.edit_data_record, name='edit_data_record'),
    path('edit_data_record/<int:ref_id>/', data_views.edit_data_record, name='edit_data_record'),
    path('delete/entire-record/<int:ref_id>/confirm/', data_views.delete_entire_record_confirm, name='delete_entire_record_confirm'),
    path('delete/datacr-record/<int:cr_id>/confirm/', data_views.delete_datacr_record_confirm, name='delete_datacr_record_confirm'),
    path('tables_panel/', data_views.tables_panel, name='tables_panel'),
    path('get-table-data/', data_views.get_table_data, name='get_table_data'),
    path('view_all_data/', data_views.view_all_data, name='view_all_data'),
    path('view_all_data/<int:ref_id>/', data_views.view_all_data, name='view_all_data'),
    path('view_all_data/<int:ref_id>/<cr_id>', data_views.view_all_data, name='view_all_data'),

    # Reporting
    path('all_reports/', report_views.all_reports, name='all_reports'),
    path('report_user/', report_views.report_user, name='report_user'),
    path('report_authors/', report_views.report_authors, name='report_authors'),
    path('reference/', report_views.reference, name='reference'),
    path('download_summaries/', report_views.download_summaries, name='download_summaries'),
    path('view_summary_results/', data_views.view_summary_results, name='view_summary_results'),

    # Add/Edit Data
    path('article-search/', data_views.article_title_search, name='article-search'),
    path('get_correction_factor/', data_views.get_correction_factor, name='get_correction_factor'),
    path('get-media-for-habitat/', data_views.get_media_for_habitat, name='get_media_for_habitat'),
    path('add_datacr/', data_views.add_datacr, name='add_datacr'),

    # Legal
    path('privacy_policy/', legal_views.privacy_policy, name='privacy_policy'),
    path('legal_disclaimer/', legal_views.legal_disclaimer, name='legal_disclaimer'),
    path('legal/', legal_views.legal_view, name='legal'),
    path('contact/', legal_views.contact, name='contact'),
]
