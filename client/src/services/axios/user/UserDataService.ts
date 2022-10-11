import { IsAuthenticated } from "../../../main";
import http from "../http-common";
class UserDataService {
	errorMessage = "Error in User Data Service: ";

	public async getById(id: number) {
		try {
			return await (
				await http.get(`/users?id=${id}`)
			).data.results;
		} catch (err) {
			console.error(this.errorMessage + err);
		}
	}

	public async getMyProfile() {
		try {
			return await (
				await http.get("myprofile/")
			).data.results;
		} catch (err) {
			IsAuthenticated(err)
			console.error(this.errorMessage + err);
		}
	}
}

const userDataService = new UserDataService();
export default userDataService;
