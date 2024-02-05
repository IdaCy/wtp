from django.contrib import admin
from django.urls import path
from dashboard_app import views as dashboard_views
# from data_app.views import GetCorrectionFactorView
from data_app import views as data_views
from manageuser_app import views as manageuser_views
from legal_app import views as legal_views
from report_app import views as report_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('view_editable_data_records/', data_views.view_editable_data_records, name='view_editable_data_records'),
    path('edit_data_record/<int:ref_id>/', data_views.edit_data_record, name='edit_data_record'),
    path('get-media-for-habitat/', data_views.get_media_for_habitat, name='get_media_for_habitat'),
    # path('get_correction_factor/', GetCorrectionFactorView.as_view(), name='get_correction_factor'),
    path('get_correction_factor/', data_views.GetCorrectionFactorView.as_view(), name='get_correction_factor'),
    path('dashboard/', dashboard_views.board_view, name='dashboard'),
    path('register/', manageuser_views.register_view, name='register'),
    path('login/', manageuser_views.login_view, name='login'),
    path('logout/', manageuser_views.logout_view, name='logout'),
    path('privacy/', manageuser_views.privacy_view, name='privacy'),
    path('legal/', manageuser_views.legal_view, name='legal'),
    path('data/', data_views.data_view, name='data'),
    path('download_summaries/', data_views.download_summaries, name='download_summaries'),
    path('view_summary_results/', data_views.view_summary_results, name='view_summary_results'),
    path('reference/', data_views.ref_view, name='reference'),
    path('add_datacr/', data_views.add_datacr, name='add_datacr'),
    path('view_all_data/', data_views.view_all_data, name='view_all_data'),
    path('view_all_data/<int:ref_id>/', data_views.view_all_data, name='view_all_data'),
    path('prev_ref_record/<int:ref_id>/', data_views.prev_ref_record, name='prev_ref_record'),
    path('next_ref_record/<int:ref_id>/', data_views.next_ref_record, name='next_ref_record'),
    path('prev_datacr_record/<int:ref_id>/<int:cr_id>/', data_views.prev_datacr_record, name='prev_datacr_record'),
    path('next_datacr_record/<int:ref_id>/<int:cr_id>/', data_views.next_datacr_record, name='next_datacr_record'),
    path('privacy_policy/', legal_views.privacy_policy, name='privacy_policy'),
    path('legal_disclaimer/', legal_views.legal_disclaimer, name='legal_disclaimer'),
    path('contact/', legal_views.contact, name='contact'),
    path('all_reports/', report_views.all_reports, name='all_reports'),
]
